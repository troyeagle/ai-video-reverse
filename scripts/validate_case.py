"""Check slide data, transcript coverage and standalone HTML integrity."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', default='BV1MssN6ZE1v')
parser.add_argument('--case-dir', type=Path)
args = parser.parse_args()
case = args.case_dir or ROOT / 'cases' / args.case
presentation = case / 'interactive-slides'
deck = json.loads((presentation / 'slides-data.json').read_text())

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.data = []
        self.external_scripts = []
        self.image_count = 0
        self.ids = set()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'script':
            self.capture = attrs.get('id') == 'deck-data'
            if attrs.get('src'):
                self.external_scripts.append(attrs['src'])
        if tag in {'img', 'canvas', 'image'}:
            self.image_count += 1
        if tag == 'use' and attrs.get('href', '').startswith('#'):
            self.references.append(attrs['href'][1:])

    def handle_endtag(self, tag):
        if tag == 'script':
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.data.append(data)

doc = Document()
doc.feed((presentation / 'index.html').read_text())
assert json.loads(''.join(doc.data)) == deck, 'Embedded data differs from sidecar JSON'
assert not doc.external_scripts, 'Runtime scripts must be embedded'
assert doc.image_count == 0, 'Presentation must use independent vector/DOM elements'
assert set(doc.references) <= doc.ids, 'Unresolved SVG symbol references'

slides = deck['slides']
assert slides and slides[0]['start'] == 0
assert slides[-1]['end'] == deck['duration']
cues = []
for index, slide in enumerate(slides):
    assert slide['id'] == index + 1
    assert slide['start'] < slide['end']
    if index:
        assert slides[index - 1]['end'] == slide['start'], 'Gap or overlap in page ranges'
    if not slide['cues']:
        assert slide.get('narration_free') is True and slide.get('empty_reason'), f'Page {index + 1} needs an explicit silent-page reason'
    for cue in slide['cues']:
        assert 0 <= cue['start'] < cue['end'] <= deck['duration']
        assert cue['text'].strip()
        cues.append(cue)
assert len({(c['start'], c['end'], c['text']) for c in cues}) == len(cues), 'Duplicate transcript records'
assert all(a['start'] <= b['start'] for a, b in zip(cues, cues[1:]))

source = json.loads((case / '校订转写.json').read_text())['segments']
normalize = lambda text: ''.join(c for c in text if c.isalnum())
assert normalize(''.join(c['text'] for c in cues)) == normalize(''.join(c['text'] for c in source)), 'Delivered transcript does not preserve the complete corrected source text'

if args.case == 'BV1MssN6ZE1v':
    assert len(slides) == 32
    assert len({s['title'] for s in slides}) == 19
    assert len(cues) == 81
    assert slides[0]['title'] == '财政的钱，为什么还是不够？'
    assert slides[1]['title'] == '多收的钱，填不满缺口'
print(json.dumps({'case': case.name, 'slides': len(slides), 'title_layouts': len({s['title'] for s in slides}), 'transcript_rows': len(cues), 'duration': deck['duration'], 'source_text_complete': True, 'embedded_data_equal': True, 'external_scripts': len(doc.external_scripts), 'raster_elements': doc.image_count}, ensure_ascii=False, indent=2))
