import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('static_pages', ROOT / 'scripts/build_static_pages.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class StaticPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = builder.build_site(Path(cls.temp.name) / 'dist')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_export_contains_only_registered_html(self):
        names = {p.relative_to(self.output).as_posix() for p in self.output.rglob('*') if p.is_file()}
        self.assertEqual(names, {'index.html', 'BV1MssN6ZE1v/index.html'})

    def test_online_deck_preserves_all_slide_data(self):
        html = (self.output / 'BV1MssN6ZE1v/index.html').read_text()
        from html.parser import HTMLParser
        class DeckData(HTMLParser):
            def __init__(self): super().__init__(); self.capture = False; self.parts = []
            def handle_starttag(self, tag, attrs):
                if tag == 'script': self.capture = dict(attrs).get('id') == 'deck-data'
            def handle_endtag(self, tag):
                if tag == 'script': self.capture = False
            def handle_data(self, data):
                if self.capture: self.parts.append(data)
        parser = DeckData(); parser.feed(html)
        self.assertEqual(json.loads(''.join(parser.parts)), json.loads((ROOT / 'cases/BV1MssN6ZE1v/interactive-slides/slides-data.json').read_text()))

    def test_online_deck_never_requests_ignored_local_audio(self):
        html = (self.output / 'BV1MssN6ZE1v/index.html').read_text()
        self.assertIn('data-local-only="true"', html)
        self.assertNotIn('src="narration.m4a"', html)
        self.assertIn('原声仅本地提供', html)
        self.assertIn('src="narration.m4a"', (ROOT / 'cases/BV1MssN6ZE1v/interactive-slides/index.html').read_text())

    def test_directory_entry_uses_relative_case_links(self):
        self.assertIn('href="BV1MssN6ZE1v/"', (self.output / 'index.html').read_text())

    def test_duplicate_or_traversal_case_ids_are_rejected(self):
        for cases in [['../private'], ['BV1MssN6ZE1v', 'BV1MssN6ZE1v'], []]:
            with self.subTest(cases=cases), tempfile.TemporaryDirectory() as temp:
                root = Path(temp); (root / '.github').mkdir()
                (root / '.github/static-pages.json').write_text(json.dumps({'schema': 1, 'cases': cases}))
                with self.assertRaises(ValueError): builder.load_cases(root)


if __name__ == '__main__':
    unittest.main()
