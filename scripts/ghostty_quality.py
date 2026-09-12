"""Offline checks of captured Ghostty command frames; never acquires a screen."""
import argparse
from collections import Counter
from io import BytesIO
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageCms
from ithilienlib import load_palette, wcag


def rgb(value):
    return tuple(bytes.fromhex(value.lstrip('#')))


def srgb_image(path):
    image=Image.open(path)
    if image.info.get('icc_profile'):
        image=ImageCms.profileToProfile(image, ImageCms.ImageCmsProfile(BytesIO(image.info['icc_profile'])),
                                       ImageCms.createProfile('sRGB'), outputMode='RGB')
    return image.convert('RGB')


def grid(image, colors):
    """Find the six contiguous six-cell calibration bars, outside app chrome."""
    lookup={rgb(c):i for i,c in enumerate(colors)}
    for y in range(image.height//2):
        runs=[]; last=None
        for x in range(image.width):
            index=lookup.get(image.getpixel((x,y)))
            if index != last:
                if last is not None:runs[-1][2]=x
                if index is not None:runs.append([index,x,image.width])
                last=index
        for start in range(max(0,len(runs)-5)):
            band=runs[start:start+6]
            if [r[0] for r in band]!=list(range(6)):continue
            widths=[r[2]-r[1] for r in band]
            if min(widths)<12 or max(widths)-min(widths)>2:continue
            if any(band[i][2]!=band[i+1][1] for i in range(5)):continue
            bottom=y
            centers=[(r[1]+r[2])//2 for r in band]
            while bottom<image.height and all(lookup.get(image.getpixel((x,bottom)))==i for i,x in enumerate(centers)):
                bottom+=1
            if bottom-y<8:continue
            return {'x':band[0][1],'y':y,'cell_width':sum(widths)/36,'cell_height':bottom-y}
    raise ValueError('Calibration grid not found; blank, clipped, or incompatible capture')


def ansi_cells(data, palette, columns=120):
    ansi=list(palette['ansi'].values());default=palette['foregrounds']['text']
    fg=default; row=0; col=0; cells=[]; lines=['']
    for part in re.split(r'(\x1b\[[0-9;]*m)',data):
        if re.fullmatch(r'\x1b\[[0-9;]*m',part):
            codes=[int(c or 0) for c in part[2:-1].split(';')];i=0
            while i<len(codes):
                n=codes[i]
                if n in (0,39):fg=default
                elif 30<=n<=37:fg=ansi[n-30]
                elif 90<=n<=97:fg=ansi[n-90+8]
                elif n==38 and codes[i+1:i+2]==[5]:
                    value=codes[i+2]
                    if value>=16:raise ValueError('Fixture uses unsupported indexed color')
                    fg=ansi[value];i+=2
                elif n==38 and codes[i+1:i+2]==[2]:
                    fg='#'+''.join(f'{v:02X}' for v in codes[i+2:i+5]);i+=4
                elif n not in (1,2,3,4,22,23,24,49):raise ValueError(f'Unsupported fixture SGR {n}')
                i+=1
            continue
        for char in part:
            if char=='\r':col=0;continue
            if char=='\n':row+=1;col=0;lines.append('');continue
            if not 32<=ord(char)<127:raise ValueError('Unsupported non-ASCII/control fixture character')
            if col==columns:row+=1;col=0;lines.append('')
            cells.append({'row':row,'column':col,'text':char,'fg':fg})
            lines[-1]+=char;col+=1
    return cells, lines


def normalize(text):
    # Only whitespace is normalized; punctuation and operators must remain exact.
    return ''.join(text.split())


def content_gate(lines, observations, geometry, height):
    missing=[]
    for row,line in enumerate(lines):
        if not line.strip():continue
        top=geometry['y']+(row+2)*geometry['cell_height']
        candidates=[]
        for item in observations:
            _,y,_,h=item['box'];center=height*(1-y-h/2)
            if top<=center<top+geometry['cell_height']:
                candidates.append(item)
        candidates.sort(key=lambda item:item['box'][0])
        observed=''.join(item['text'] for item in candidates)
        if normalize(line)!=normalize(observed):
            missing.append({'row':row,'expected':line,'observed':observed})
    return {'status':'unverified' if missing else 'pass','mismatches':missing,
            'scope':'Strict OCR line comparison except whitespace; mismatches need review and never count as passing.'}


def luminance(color):
    values=[v/255 for v in color]
    values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(a*b for a,b in zip(values,(.2126,.7152,.0722)))


def cell_checks(image, geometry, cells, background):
    findings=[];ratios=[]
    for cell in cells:
        if cell['text']==' ':continue
        x=round(geometry['x']+cell['column']*geometry['cell_width'])
        y=geometry['y']+(cell['row']+2)*geometry['cell_height']
        w=round(geometry['cell_width']);h=geometry['cell_height']
        if x<0 or y<0 or x+w>image.width or y+h>image.height:
            findings.append({**cell,'reason':'clipped cell'});continue
        raw=image.crop((x,y,x+w,y+h)).tobytes()
        counts=Counter(zip(raw[::3],raw[1::3],raw[2::3]))
        bg,count=counts.most_common(1)[0]
        # Use solid dark stroke pixels; a fixed area percentile penalizes tiny punctuation.
        ink=next((color for color,n in sorted(counts.items(),key=lambda p:luminance(p[0])) if n>=2), bg)
        ratio=(luminance(bg)+.05)/(luminance(ink)+.05)
        ratios.append(ratio)
        matching=sum(n for color,n in counts.items() if max(abs(a-b) for a,b in zip(color,rgb(cell['fg'])))<=3)
        if max(abs(a-b) for a,b in zip(bg,rgb(background)))>3:
            findings.append({**cell,'reason':'unexpected cell background','observed':bg})
        elif ratio<4.5:
            findings.append({**cell,'reason':'low rendered contrast','contrast':round(ratio,3)})
        elif matching<2:
            findings.append({**cell,'reason':'expected foreground missing'})
    return {'status':'fail' if findings else 'pass','minimum_contrast':round(min(ratios),3) if ratios else None,
            'findings':findings,'scope':'ASCII nonspace cell coverage and dark stroke ink versus modal background; 4.5 floor. This is a rendering proxy, not a comfort score.'}


def prepare_ocr_rows(image, geometry, lines, output):
    """Isolate complete terminal rows; never send expected text to the OCR engine."""
    output.mkdir(parents=True, exist_ok=True)
    manifest=[]
    for row,line in enumerate(lines):
        if not line.strip():continue
        top=geometry['y']+(row+2)*geometry['cell_height']
        bottom=top+geometry['cell_height']
        if bottom>image.height:
            raise ValueError(f'Expected row {row} is clipped')
        # Full terminal width, not the expected string length. Preserve unexpected suffixes.
        crop=image.crop((geometry['x'],top,image.width,bottom))
        crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.LANCZOS)
        padded=Image.new('RGB',(crop.width+48,crop.height+48),image.getpixel((image.width-1,top)))
        padded.paste(crop,(24,24))
        path=output/f'row-{row:03}.png';padded.save(path)
        manifest.append({'row':row,'path':str(path.resolve())})
    path=output/'rows.json';path.write_text(json.dumps(manifest,indent=2))
    return path


def row_content_gate(lines, recognized):
    rows={item['row']:item for item in recognized}
    mismatches=[]
    for row,line in enumerate(lines):
        if not line.strip():continue
        observed=''.join(f['text'] for f in rows.get(row,{}).get('fragments',[]))
        if normalize(line)!=normalize(observed):
            mismatches.append({'row':row,'expected':line,'observed':observed})
    return {'status':'unverified' if mismatches else 'pass','mismatches':mismatches,
            'scope':'Isolated full-width rows, 2x scaling and padding; top OCR candidate only. Only whitespace normalized; no expected-text hints or punctuation substitutions.'}


def assess_capture(image_path, ansi_path, helper, palette, reference=None):
    image=srgb_image(image_path)
    colors=list(palette['ansi'].values())[1:7]
    geometry=grid(image,colors)
    cells,lines=ansi_cells(ansi_path.read_text(),palette)
    pixels=cell_checks(image,geometry,cells,palette['backgrounds']['base'])
    try:
        manifest=prepare_ocr_rows(image,geometry,lines,image_path.parent/'ocr-rows'/image_path.stem)
        process=subprocess.run([str(helper),'ocr-rows',str(manifest)],capture_output=True,text=True,check=True,timeout=60)
        ocr=json.loads(process.stdout)
        content=row_content_gate(lines,ocr['rows'])
    except (subprocess.SubprocessError, OSError) as exc:
        ocr={'error':getattr(exc,'stderr',None) or str(exc)}
        content={'status':'unverified','reason':'OCR unavailable: '+ocr['error']}
    if reference and content.get('mismatches'):
        from ghostty_glyphs import recover_content
        try:
            content=recover_content(content,image,geometry,*reference)
        except ValueError as exc:
            content['glyph_error']=str(exc)
    return {'status':'fail' if pixels['status']=='fail' else content['status'], 'geometry':geometry,
            'content':content,'text_pixels':pixels,'ocr':ocr,
            'image_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest(),
            'ansi_sha256':hashlib.sha256(ansi_path.read_bytes()).hexdigest()}


def analyze(output, helper):
    report=json.loads((output/'report.json').read_text());palette=load_palette('ithilien-dawn')
    if report['theme_sha256']!=hashlib.sha256((Path(__file__).resolve().parents[1]/'ghostty/themes/ithilien_dawn.conf').read_bytes()).hexdigest():
        raise ValueError('Capture theme differs from current theme; refusing stale palette analysis')
    results=[]
    prepared={r['id']:r for r in report['results']}
    reference=None; reference_sha=None
    from ghostty_glyphs import reference_sheet
    expected_atlas=hashlib.sha256(reference_sheet()[0].encode()).hexdigest()
    for frame in report.get('native_captures',[]):
        if frame['id']=='glyph-reference' and 'image' in frame:
            source=output/prepared[frame['id']]['ansi']
            if hashlib.sha256(source.read_bytes()).hexdigest()!=expected_atlas or prepared[frame['id']]['sha256']!=expected_atlas:
                raise ValueError('Native glyph reference payload is stale or changed')
            reference_image=srgb_image(output/frame['image'])
            reference=(reference_image,grid(reference_image,list(palette['ansi'].values())[1:7]))
            reference_sha=hashlib.sha256((output/frame['image']).read_bytes()).hexdigest()
    for frame in report.get('native_captures',[]):
        if frame['id']=='glyph-reference':continue
        if 'image' not in frame:continue
        source=output/prepared[frame['id']]['ansi']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=prepared[frame['id']]['sha256']:
            raise ValueError('ANSI fixture changed since capture')
        try:result=assess_capture(output/frame['image'],source,helper,palette,reference)
        except (ValueError,OSError,subprocess.SubprocessError) as exc:result={'status':'unverified','reason':str(exc)}
        result['id']=frame['id'];results.append(result)
    expected={r['id'] for r in report['results'] if r['status']=='prepared' and r.get('kind')!='glyph-reference'}
    missing=sorted(expected-{r['id'] for r in results})
    summary={'status':'pass' if results and not missing and all(r['status']=='pass' for r in results) else 'not_passed',
             'missing_captures':missing,
             'results':results,'scope':'Offline analysis of previously captured command frames. Does not certify cursor, selection, font, or full native workflows.'}
    summary['glyph_reference_sha256']=reference_sha
    summary['glyph_classifier_sha256']=hashlib.sha256((Path(__file__).parent/'ghostty_glyphs.py').read_bytes()).hexdigest()
    summary['analyzer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary['helper_sha256']=hashlib.sha256(helper.read_bytes()).hexdigest() if helper.exists() else None
    (output/'quality.json').write_text(json.dumps(summary,indent=2))
    rows=''.join('<tr><td>'+html.escape(r['id'])+'</td><td>'+html.escape(r['status'])+'</td><td>'+str(r.get('text_pixels',{}).get('minimum_contrast'))+'</td><td>'+str(len(r.get('text_pixels',{}).get('findings',[])))+'</td><td>'+html.escape(r.get('content',{}).get('status','unverified'))+'</td></tr>' for r in results)
    (output/'quality.html').write_text('<!doctype html><meta charset="utf-8"><title>Ghostty text checks</title><style>body{font:16px system-ui;padding:30px}td,th{padding:12px;text-align:left}</style><h1>Ghostty command text checks</h1><p>Pixel checks and strict OCR are independent. OCR mismatches are unverified, not proof of a palette defect. The attribute probe intentionally includes ANSI white on the light canvas; these incompatible pairs remain visible findings.</p><table><tr><th>Case</th><th>Status</th><th>Minimum ink contrast</th><th>Pixel findings</th><th>Text completeness</th></tr>'+rows+'</table><p><a href="quality.json">Detailed evidence</a> · <a href="gallery.html">Screenshots</a></p><p>Cursor, selection, font verification and long-session comfort remain untested.</p>')
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--helper',type=Path,required=True)
    args=parser.parse_args()
    summary=analyze(args.output.resolve(),args.helper.resolve())
    print(json.dumps({'status':summary['status'],'cases':[(r['id'],r['status']) for r in summary['results']]},indent=2))
    raise SystemExit(0 if summary['status']=='pass' else 1)
