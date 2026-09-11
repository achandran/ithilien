"""Generate the README palette chart directly from canonical named colors."""
from unittest.mock import patch
import review_day
from ithilienlib import ROOT, load_palette, load_palette_source


def generate_chart():
    source = load_palette_source('ithilien-dawn')
    p = load_palette('ithilien-dawn')
    d = review_day.Drawing()
    width, height = 1200, 840
    d.rect(0, 0, width, height, p['backgrounds']['base'])
    d.text(24, 20, 'ITHILIEN DAWN', p['foregrounds']['text'], 'bold')
    for i, (name, color) in enumerate(source['colors'].items()):
        x, y = 24 + (i % 5) * 234, 68 + (i // 5) * 128
        d.rect(x, y, 216, 58, p['backgrounds']['border'])
        d.rect(x + 1, y + 1, 214, 56, color)
        d.text(x, y + 67, name, p['foregrounds']['text'], 'bold')
        d.text(x, y + 91, color, p['foregrounds']['muted'])
    destination = ROOT/'assets'
    destination.mkdir(exist_ok=True)
    with patch.object(review_day, 'OUT', destination):
        d.save('ithilien-dawn-palette', width, height, False)
    return d


if __name__ == '__main__':
    generate_chart()
