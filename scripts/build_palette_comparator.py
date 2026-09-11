"""Build a file:// compatible A/B viewer from existing native-cell galleries."""
import json,re,sys,html
from pathlib import Path
out=Path(sys.argv[1]);assets=out/'comparison-assets';assets.mkdir(exist_ok=True)
variants=['candidate-00','candidate-04','candidate-06','candidate-10']
paths={'Neovim':'neovim/gallery.html','Python TS/LSP':'python/gallery.html','Codex diffs':'codex/ithilien-dawn/diff/codex-gallery.html','Codex flows':'codex/ithilien-dawn/flows/codex-gallery.html'}
frames={}
for suite,path in paths.items():
 for variant in variants:
  s=(out/variant/path).read_text()
  pattern=r'<summary>(.*?)</summary>.*?(<pre>.*?</pre>)' if suite in ('Neovim','Python TS/LSP') else r'<h2>(.*?)</h2>\s*(<pre>.*?</pre>)'
  for label,pre in re.findall(pattern,s,re.S):frames.setdefault((suite,html.unescape(label)),{})[variant]=pre
index=[]
for i,((suite,label),data) in enumerate(frames.items()):
 assert set(data)==set(variants),(suite,label)
 filename=f'comparison-assets/{i}.js'
 (out/filename).write_text('window.deliverFrame('+json.dumps(i)+','+json.dumps(data)+');')
 index.append({'id':i,'suite':suite,'label':label,'src':filename})
page='''<!doctype html><meta charset="utf-8"><title>Ithilien A/B comparison</title>
<style>body{margin:0;background:#eee;color:#222;font:15px system-ui}header{padding:16px;position:sticky;top:0;background:#fff;z-index:1;border-bottom:1px solid #aaa}select,button{font:inherit;padding:7px;margin:4px}main{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px}main.single{grid-template-columns:1fr}article{min-width:0}h2{font-size:16px}.screen{overflow:auto;max-height:75vh;background:#F6F6F3}pre{font:16pt/1.4 "Berkeley Mono Medium",monospace;margin:0;width:max-content}p{margin:6px 0}.hidden{display:none}button:focus-visible,select:focus-visible{outline:3px solid #345e77}</style>
<header><strong>Ithilien Dawn — same native capture, different palettes</strong><p>16pt Berkeley Mono Medium requested. HTML reconstruction, not a Ghostty screenshot. Scroll is synchronized.</p>
<label>Suite <select id="suite"></select></label><label>Fixture / width / state <select id="fixture"></select></label><br>
<label>A <select id="a"></select></label><label>B <select id="b"></select></label><button id="mode">Switch to A/B toggle</button><button id="toggle">Show B (Space)</button><span id="status" role="status"></span>
</header><main id="panes"><article><h2 id="titleA"></h2><div class="screen" id="screenA"></div></article><article id="articleB"><h2 id="titleB"></h2><div class="screen" id="screenB"></div></article></main>
<script>
const frames=INDEX, names={'candidate-00':'Baseline','candidate-04':'04 · stronger blue','candidate-06':'06 · stronger blue + deeper amber','candidate-10':'10 · strongest blue + deeper amber'};
const $=id=>document.getElementById(id);let data=null,requested=null,single=false,showB=false;
for(const suite of [...new Set(frames.map(f=>f.suite))])$('suite').add(new Option(suite,suite));
for(const id of ['a','b'])for(const [value,label] of Object.entries(names))$(id).add(new Option(label,value));$('b').value='candidate-04';
function render(){if(!data)return;let x=$('a').value,y=$('b').value;const left=$('screenA').scrollLeft,top=$('screenA').scrollTop;
$('screenA').innerHTML=data[single&&showB?y:x];$('screenB').innerHTML=data[y];$('titleA').textContent=(single&&showB?'B: ':'A: ')+names[single&&showB?y:x];$('titleB').textContent='B: '+names[y];$('articleB').classList.toggle('hidden',single);$('panes').classList.toggle('single',single);$('toggle').disabled=!single;$('toggle').textContent=showB?'Show A (Space)':'Show B (Space)';$('mode').textContent=single?'Switch to side by side':'Switch to A/B toggle';for(const id of ['screenA','screenB']){$(id).scrollLeft=left;$(id).scrollTop=top;}}
window.deliverFrame=(id,value)=>{if(id!==requested)return;data=value;render();$('status').textContent='Loaded';};
function load(){data=null;requested=Number($('fixture').value);$('status').textContent='Loading…';for(const id of ['screenA','screenB'])$(id).innerHTML='';const s=document.createElement('script');s.src=frames[requested].src;s.onerror=()=>{$('status').textContent='Capture could not load';};document.body.append(s);}
function fixtures(){$('fixture').innerHTML='';for(const f of frames.filter(f=>f.suite===$('suite').value))$('fixture').add(new Option(f.label,f.id));load();}
$('suite').onchange=fixtures;$('fixture').onchange=load;$('a').onchange=render;$('b').onchange=render;$('mode').onclick=()=>{single=!single;render();};$('toggle').onclick=()=>{showB=!showB;render();};document.onkeydown=e=>{if(e.code==='Space'&&!['SELECT','BUTTON','INPUT'].includes(document.activeElement.tagName)&&single){e.preventDefault();showB=!showB;render();}};
for(const [a,b] of [['screenA','screenB'],['screenB','screenA']])$(a).onscroll=()=>{if($(b).scrollLeft!==$(a).scrollLeft)$(b).scrollLeft=$(a).scrollLeft;if($(b).scrollTop!==$(a).scrollTop)$(b).scrollTop=$(a).scrollTop;};fixtures();
</script>'''.replace('INDEX',json.dumps(index))
(out/'compare.html').write_text(page)
p=out/'index.html';s=p.read_text();link='<p><a href="compare.html">Open synchronized side-by-side / A-B comparison</a></p>'
if link not in s:s=s.replace('<h1>Ithilien Dawn: bounded palette experiment</h1>','<h1>Ithilien Dawn: bounded palette experiment</h1>'+link);p.write_text(s)
print(len(index),'matched captures across',len(variants),'variants')
