import sys,json,itertools
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
from ithilienlib import wcag,delta_e,oklch
p=json.loads(Path('palette/ithilien-dawn.json').read_text()); c=p['colors']
families=['red','green','yellow','blue','magenta','cyan']
options=[['Briar'],['Fir','Sage'],['Filbert','Broom'],['Eventide','Anduin'],['Hyacinth','Thyme'],['Stillwater','Poros']]
surfaces={k:c[p['backgrounds'][k]] for k in ['base','mantle','surface0','surface1']}
rows=[]
for names in itertools.product(*options):
    colors=dict(zip(families,[c[n] for n in names]))
    pairs=list(itertools.combinations(families,2))
    distances={s:{f'{a}/{b}':delta_e(colors[a],colors[b],s) for a,b in pairs} for s in ['normal','protan','deutan','tritan']}
    rows.append({'names':names,'colors':colors,'contrast_base':{k:wcag(v,surfaces['base']) for k,v in colors.items()},'minimum_surface_contrast':min(wcag(v,bg) for v in colors.values() for bg in surfaces.values()),'minimum_distance':{s:min(ds.values()) for s,ds in distances.items()},'red_green_distance':{s:ds['red/green'] for s,ds in distances.items()},'black_separation':min(delta_e(v,'#000000') for v in colors.values()),'distances':distances})
out=Path(__file__).resolve().parent
(out/'measurements.json').write_text(json.dumps({'metric':'OKLab Euclidean distance; diagnostic, not validated usability score','surfaces':surfaces,'candidates':rows},indent=2))
for r in [rows[0],rows[-1],max(rows,key=lambda r:r['minimum_distance']['normal'])]:
 print(json.dumps({k:v for k,v in r.items() if k!='distances'},indent=2))
print('top normal separation')
for r in sorted(rows,key=lambda r:r['minimum_distance']['normal'],reverse=True)[:5]:print(r['names'],r['minimum_distance'],r['minimum_surface_contrast'])
