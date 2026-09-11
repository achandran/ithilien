"""Isolated design study. Does not modify published palettes or exports."""
import json, pathlib, hashlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
base=json.loads((ROOT/'palette/ithilien-dawn.json').read_text())
shared={'Lebethron':'#25292B','Ash':'#596166','Stonecrop':'#76848B','Rosehip':'#A3373E','Sage':'#315F46','Anduin':'#345E77','Broom':'#795922','Thyme':'#70516D','Poros':'#306466','Pelennor':'#E2EDDF','Ilex':'#BDD3B2','Eglantine':'#F1E2DF','Rose':'#DDAFA7','Spray':'#E0E9EE','Harlond':'#B3CBD8','Celandine':'#EAD9B1','Clematis':'#E5D9E7','Juniper':'#3F535F'}
roles={'canvas':'Asphodel','chrome':'Gondor','raised':'Lily','line':'Anemone','text':'Lebethron','secondary':'Ash','border':'Stonecrop','accent':'Rosehip','error':'Rosehip','success':'Sage','info':'Anduin','warning':'Broom','hint':'Poros','purple':'Thyme','selection':'Harlond','selectionText':'Lebethron','selectionBorder':'Juniper','add':'Pelennor','addEmphasis':'Ilex','delete':'Eglantine','deleteEmphasis':'Rose','change':'Spray','changeEmphasis':'Harlond','search':'Celandine','conflict':'Clematis'}
choices=[('neutral','A · Neutral white',{'Asphodel':'#F6F6F3','Gondor':'#E0E3E2','Lily':'#FDFDFA','Anemone':'#ECEEEB'}),('mineral','B · Mineral white',{'Asphodel':'#F0F1EC','Gondor':'#DDE1DC','Lily':'#F8F9F4','Anemone':'#E6E9E3'}),('steel','C · Cool steel white',{'Asphodel':'#EFF3F5','Gondor':'#DCE3E7','Lily':'#F8FBFC','Anemone':'#E5EBEE'})]
def lum(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    c=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in c]
    return sum(x*w for x,w in zip(c,[.2126,.7152,.0722]))
def contrast(a,b):
    x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
allp={};audit={}
for slug,label,surfaces in choices:
    colors={**shared,**surfaces}
    p={'name':'Ithilien Dawn','candidate':slug,'label':label,'colors':colors,'roles':roles,'colorNotes':{k:base['colorNotes'][k] for k in colors}}
    (OUT/f'{slug}.json').write_text(json.dumps(p,indent=2)+'\n')
    r={k:colors[v] for k,v in roles.items()};allp[slug]={'label':label,**r};checks=[]
    def check(fg,bg,target):
        n=contrast(r[fg],r[bg]);checks.append({'foreground':fg,'background':bg,'ratio':round(n,3),'target':target});assert n>=target,(slug,fg,bg,n)
    for bg in ('canvas','chrome','raised','line','add','delete','change','search','conflict'):
        check('text',bg,7)
        check('secondary',bg,4.5)
    for fg in ('error','success','info','warning','hint','purple'):
        for bg in ('canvas','chrome','raised','line'):check(fg,bg,4.5)
    for bg in ('addEmphasis','deleteEmphasis','changeEmphasis'):check('text',bg,7)
    check('selectionText','selection',7)
    check('selectionBorder','selection',3)
    check('selectionBorder','canvas',3)
    check('border','canvas',3)
    audit[slug]=checks
(OUT/'resolved.json').write_text(json.dumps(allp,indent=2)+'\n')
(OUT/'contrast.json').write_text(json.dumps(audit,indent=2)+'\n')
print('PASS:',sum(map(len,audit.values())),'specified contrast pairs')
