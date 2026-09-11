"""Compare logical source selections/search matches to native highlight provenance."""
def overlay_failures(shot):
    state=shot['state']
    if state=='diff':return []
    if 'overlay' not in shot or 'attr_info' not in shot:return [{'gate':'overlay_metadata_missing'}]
    o=shot['overlay'];cells={(c['row'],c['col']):c for c in shot['cells']};failures=[]
    for r in shot.get('regions',[]):
        c=cells.get((r['row'],r['col']))
        if c is None:continue
        info=shot['attr_info'].get(c['attr'],shot['attr_info'].get(str(c['attr']),[]))
        names={x.get('hi_name') for x in info}
        if state=='search':
            expected=r.get('search_match',False);actual=bool(names & {'Search','CurSearch','IncSearch'})
        else:
            a=tuple(o['anchor']);b=tuple(o['finish']);lo,hi=sorted((a,b));position=(r['source_line'],r['source_byte'])
            expected=False
            if r['side']=='after':
                if state=='selection':expected=lo[0]<=position[0]<=hi[0]
                elif state=='selection-char':expected=lo<=position<=hi
                else:
                    left,right=sorted((o['anchor_vcol'],o['finish_vcol']))
                    expected=lo[0]<=position[0]<=hi[0] and r['vcol'][0]<=right and r['vcol'][1]>=left
                # Cursor glyph is rendered separately by terminal/UI, not Visual.
                if position==b:continue
            actual='Visual' in names
        if expected!=actual:
            failures.append({'gate':'overlay_missing_cell' if expected else 'overlay_extra_cell','case':shot['case'],'width':shot['width'],'state':state,'region':r,'evidence':f'gallery.html#{shot["case"]}-{shot["width"]}-{state}'})
    return failures
