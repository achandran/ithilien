"""Small SVG drawing utility for generated palette assets."""
import html


class Drawing:
    def __init__(self): self.commands=[]
    def rect(self,x,y,w,h,color): self.commands.append(dict(x=x,y=y,w=w,h=h,color=color))
    def text(self,x,y,text,color,style='regular'): self.commands.append(dict(x=x,y=y,text=text,color=color,style=style))
    def save(self, path, width, height):
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<style>text{font-family:"Berkeley Mono Medium",monospace;font-size:16pt}</style>']
        for c in self.commands:
            if 'text' in c:
                style='font-weight="700" font-style="italic"' if c['style']=='bold-italic' else 'font-weight="700"' if c['style']=='bold' else 'font-style="italic"' if c['style']=='italic' else ''
                svg.append(f'<text x="{c["x"]}" y="{c["y"]+15}" fill="{c["color"]}" {style}>{html.escape(c["text"])}</text>')
            else: svg.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" fill="{c["color"]}"/>')
        path.write_text('\n'.join(svg+['</svg>']))
