import sys
from pathlib import Path
import pytest
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ghostty_quality import ansi_cells, grid, cell_checks, content_gate
from ithilienlib import load_palette


def specimen():
    p=load_palette('ithilien-dawn')
    im=Image.new('RGB',(400,100),p['backgrounds']['base'])
    draw=ImageDraw.Draw(im)
    for i,c in enumerate(list(p['ansi'].values())[1:7]):
        draw.rectangle((i*60,0,i*60+59,19),fill=c)
    draw.rectangle((2,44,5,55),fill='#000000')
    return im,p


def test_grid_rejects_blank_image_and_missing_calibration_band():
    im,p=specimen();colors=list(p['ansi'].values())[1:7]
    assert grid(im,colors)=={'x':0,'y':0,'cell_width':10,'cell_height':20}
    for damaged in (Image.new('RGB',im.size,'white'), im.crop((0,0,300,100))):
        with pytest.raises(ValueError,match='Calibration grid'):grid(damaged,colors)


def test_erased_glyph_and_low_contrast_cannot_pass():
    im,p=specimen();g=grid(im,list(p['ansi'].values())[1:7]);cells=[{'row':0,'column':0,'text':'a','fg':'#000000'}]
    assert cell_checks(im,g,cells,p['backgrounds']['base'])['status']=='pass'
    for color in (p['backgrounds']['base'],'#EEEEEE'):
        damaged=im.copy();ImageDraw.Draw(damaged).rectangle((0,40,9,59),fill=color)
        assert cell_checks(damaged,g,cells,p['backgrounds']['base'])['status']=='fail'
    assert cell_checks(im.crop((0,0,400,45)),g,cells,p['backgrounds']['base'])['findings'][0]['reason']=='clipped cell'


def test_small_punctuation_with_solid_strokes_is_not_area_penalized():
    im,p=specimen();g=grid(im,list(p['ansi'].values())[1:7])
    draw=ImageDraw.Draw(im);draw.rectangle((0,40,9,59),fill=p['backgrounds']['base'])
    draw.rectangle((3,54,4,56),fill=p['accents']['aqua'])
    assert cell_checks(im,g,[{'row':0,'column':0,'text':',','fg':p['accents']['aqua']}],p['backgrounds']['base'])['status']=='pass'


def test_ocr_requires_operator_and_every_line():
    g={'y':0,'cell_height':10}
    observed=[{'text':'return attempt <= 3','box':[0,.7,.9,.1]}]
    assert content_gate(['return attempt <= 3'],observed,g,100)['status']=='pass'
    assert content_gate(['return attempt < 3'],observed,g,100)['status']=='unverified'
    assert content_gate(['return attempt <= 3','missing'],observed,g,100)['status']=='unverified'


def test_ansi_preserves_character_positions_and_rejects_unsupported_controls():
    p=load_palette('ithilien-dawn')
    cells,lines=ansi_cells('\x1b[31m- a\x1b[0m\n+ b',p)
    assert lines==['- a','+ b']
    assert cells[2]['column']==2 and cells[2]['fg']==list(p['ansi'].values())[1]
    with pytest.raises(ValueError):ansi_cells('\x1b[2J',p)
