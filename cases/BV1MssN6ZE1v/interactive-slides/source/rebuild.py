"""Rebuild the standalone webpage from the bundled sources and data."""
import json
from pathlib import Path

source=Path(__file__).resolve().parent
dest=source.parent
deck=json.loads((dest/'slides-data.json').read_text())
html=(source/'template.html').read_text()
for token,content in [
    ('/*__STYLE__*/',(source/'style.css').read_text()),
    ('<!--__ICONS__-->',(source/'icons.svg').read_text()),
    ('/*__DATA__*/',json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')),
    ('/*__RENDER__*/',(source/'render.js').read_text()),
    ('/*__APP__*/',(source/'app.js').read_text()),
]:
    html=html.replace(token,content)
(dest/'index.html').write_text(html)
print(f'Rebuilt {len(deck["slides"])} slides: {dest / "index.html"}')
