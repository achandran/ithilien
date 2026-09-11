"""Checks on native UI captures, independent of gallery presentation."""


def effective_colors(shot, cell):
    attrs=shot['attrs'].get(cell['attr'],shot['attrs'].get(str(cell['attr']),{}))
    fg=attrs.get('foreground',shot['defaults']['fg'])
    bg=attrs.get('background',shot['defaults']['bg'])
    if attrs.get('reverse'):fg,bg=bg,fg
    return fg,bg


def state_failures(shot,palette):
    if shot.get('require_syntax') and len(shot.get('syntax_groups',[])) < 3:
        return [{'case':shot['case'],'state':shot['state'],'error':'Python syntax highlighting missing'}]
    role={'search':palette['backgrounds']['search'], 'selection':palette['highlight']['background']}.get('selection' if shot['state'].startswith('selection') else shot['state'])
    if role is None:return []
    expected=int(role[1:],16)
    matching=[c for c in shot['cells'] if c['text'] and effective_colors(shot,c)[1]==expected]
    if not matching:return [{'case':shot['case'],'state':shot['state'],'error':'Expected overlay missing from native cells'}]
    return []


def compare_reports(old,new):
    return {'new_failures':new['failures'],
            'codex_before':old.get('codex',{}),
            'codex_after':new.get('codex',{}),
            'previous_failure_count':len(old['failures']),
            'palette_changed':old['palette_sha256']!=new['palette_sha256'],
            'minimum_text_contrast_before':min((v for k,v in old['pair_contrasts'].items() if k.endswith('/4.5')),default=None),
            'minimum_text_contrast_after':min((v for k,v in new['pair_contrasts'].items() if k.endswith('/4.5')),default=None),
            'interpretation':'Contrast is not a comfort score. Inspect galleries before approving palette changes.'}
