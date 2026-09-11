"""Generate the README palette chart directly from canonical named colors."""
from unittest.mock import patch
import review_day
from ithilienlib import ROOT, load_palette, load_palette_source


def generate_chart():
    source = load_palette_source('ithilien-dawn')
    p = load_palette('ithilien-dawn')
    from ithilienlib import ROLE_FAMILIES
    labels = []
    for name in source['colors']:
        roles = [f'{family}.{role}' for family in ROLE_FAMILIES for role,ref in source[family].items() if ref==name]
        labels.append(roles[0])
    d = review_day.Drawing()
    d.rect(0, 0, 1200, 1020, p['backgrounds']['base'])
    d.text(18, 15, 'ITHILIEN DAWN', p['foregrounds']['text'], 'bold')
    d.text(18, 40, 'Named colors / sRGB / dark foregrounds / precise diffs', p['foregrounds']['subtext'])
    for i, ((name, color), label) in enumerate(zip(source['colors'].items(), labels)):
        x, y = 18 + (i % 4) * 294, 72 + (i // 4) * 94
        d.rect(x, y, 282, 84, p['backgrounds']['surface0'])
        d.rect(x + 10, y + 10, 50, 64, p['foregrounds']['comment'])
        d.rect(x + 11, y + 11, 48, 62, color)
        d.text(x + 72, y + 9, name, p['foregrounds']['text'], 'bold')
        d.text(x + 72, y + 31, color, p['foregrounds']['text'])
        d.text(x + 72, y + 55, label, p['foregrounds']['subtext'])
    destination = ROOT/'assets'
    destination.mkdir(exist_ok=True)
    with patch.object(review_day, 'OUT', destination):
        d.save('ithilien-dawn-palette', 1200, 1020, False)
    return d


if __name__ == '__main__':
    generate_chart()
