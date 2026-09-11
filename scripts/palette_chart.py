"""Generate the README palette chart directly from canonical named colors."""
from unittest.mock import patch
import review_day
from ithilienlib import ROOT, load_palette, load_palette_source


def generate_chart():
    source = load_palette_source('ithilien-dawn')
    p = load_palette('ithilien-dawn')
    d = review_day.Drawing()
    groups = [
        ('Surfaces and text', [('backgrounds.base','Canvas / popups'),('backgrounds.surface1','Soft surface'),('backgrounds.mantle','Muted surface'),('backgrounds.crust','Inset surface'),('foregrounds.text','Primary text'),('foregrounds.comment','Muted / subtext')]),
        ('Interaction', [('highlight.background','Selection / cursor'),('backgrounds.search','Search / conflict'),('backgrounds.border','Surface border')]),
        ('Diffs', [('diff.addBackground','Added line'),('diff.deleteBackground','Deleted line'),('diff.changeBackground','Changed line'),('diff.changeEmphasis','Edited characters')]),
        ('Terminal colors', [('ansi.red','Red'),('ansi.green','Green'),('ansi.yellow','Yellow'),('ansi.blue','Blue'),('ansi.magenta','Magenta'),('ansi.cyan','Cyan')]),
    ]
    columns = 4
    width = 966
    height = 60 + sum(48 + ((len(items)+columns-1)//columns)*146 for _,items in groups)
    d.rect(0, 0, width, height, p['backgrounds']['base'])
    d.text(24, 18, 'ITHILIEN DAWN / COLOR ROLES', p['foregrounds']['text'], 'bold')
    top = 66
    seen = set()
    for title, items in groups:
        d.text(24, top, title, p['foregrounds']['text'], 'bold')
        for i, (path, label) in enumerate(items):
            family, role = path.split('.')
            name = source[family][role]
            seen.add(name)
            color = source['colors'][name]
            x, y = 24 + (i % columns)*234, top + 34 + (i//columns)*146
            d.rect(x, y, 216, 48, p['backgrounds']['border'])
            d.rect(x+1, y+1, 214, 46, color)
            d.text(x, y+56, name, p['foregrounds']['text'], 'bold')
            d.text(x, y+80, label, p['foregrounds']['muted'])
            d.text(x, y+104, color, p['foregrounds']['muted'])
        top += 48 + ((len(items)+columns-1)//columns)*146
    assert seen == set(source['colors']), 'Every named color must appear in the chart'
    destination = ROOT/'assets'
    destination.mkdir(exist_ok=True)
    with patch.object(review_day, 'OUT', destination):
        d.save('ithilien-dawn-palette', width, height, False)
    return d


if __name__ == '__main__':
    generate_chart()
