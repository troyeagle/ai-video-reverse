import importlib.util
import hashlib
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
        cls.silent = builder.build_site(Path(cls.temp.name) / 'silent', include_audio=False)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_export_contains_only_registered_html_and_authorized_audio(self):
        names = {p.relative_to(self.output).as_posix() for p in self.output.rglob('*') if p.is_file()}
        expected={'index.html'} | {case+'/index.html' for case in builder.load_cases()}
        expected |= {case+'/'+name for case, (_,name) in builder.load_audio(builder.load_cases()).items()}
        self.assertEqual(names, expected)

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

    def test_silent_fallback_never_requests_ignored_local_audio(self):
        html = (self.silent / 'BV1MssN6ZE1v/index.html').read_text()
        self.assertIn('data-local-only="true"', html)
        self.assertNotIn('src="narration.m4a"', html)
        self.assertIn('原声仅本地提供', html)
        self.assertIn('src="narration.m4a"', (ROOT / 'cases/BV1MssN6ZE1v/interactive-slides/index.html').read_text())
        self.assertEqual({p.relative_to(self.silent).as_posix() for p in self.silent.rglob('*') if p.is_file()}, {'index.html'} | {case+'/index.html' for case in builder.load_cases()})

    def test_public_audio_resolves_to_verified_same_directory_asset(self):
        for case, (source,name) in builder.load_audio(builder.load_cases()).items():
            html = (self.output / case / 'index.html').read_text()
            self.assertIn(f'src="{name}"', html)
            self.assertIn('data-public-audio="true"', html)
            self.assertNotIn('data-local-only="true"', html)
            self.assertNotIn('src="narration.m4a"', html)
            self.assertEqual(hashlib.sha256((self.output/case/name).read_bytes()).digest(), hashlib.sha256(source.read_bytes()).digest())

    def test_directory_entry_uses_relative_case_links(self):
        self.assertIn('href="BV1MssN6ZE1v/"', (self.output / 'index.html').read_text())

    def test_audit_cases_export_no_private_reference_material(self):
        for case in ['BV11ts56mEVt','BV1JXxB6rErv']:
            html=(self.output/case/'index.html').read_text()
            self.assertIn('校核对照',html)
            self.assertIn('查看全片审计报告',html)
            self.assertNotIn('src="narration.m4a"',html)
            self.assertNotIn('地方财政报告参考文献.png',html)
            self.assertNotIn('sources/raw/',html)

    def test_duplicate_or_traversal_case_ids_are_rejected(self):
        for cases in [['../private'], ['BV1MssN6ZE1v', 'BV1MssN6ZE1v'], []]:
            with self.subTest(cases=cases), tempfile.TemporaryDirectory() as temp:
                root = Path(temp); (root / '.github').mkdir()
                (root / '.github/static-pages.json').write_text(json.dumps({'schema': 1, 'cases': cases}))
                with self.assertRaises(ValueError): builder.load_cases(root)

    def test_unapproved_or_changed_audio_is_rejected_before_export(self):
        case='BV11ts56mEVt'
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'.github').mkdir();(root/'public-audio').mkdir()
            source=root/'public-audio'/f'{case}.m4a'
            source.write_bytes(b'\x00\x00\x00\x10ftypM4A \x00\x00\x00\x00')
            entry={'file':f'public-audio/{case}.m4a','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bytes':source.stat().st_size,'permission':{'status':'user-confirmed','date':'2026-11-25','record':'docs/user-instructions.md'}}
            config={'schema':1,'cases':[case],'audio':{case:entry}}
            registry=root/'.github/static-pages.json'
            for field,value,reason in [('file','cases/private.m4a','exact approved'),('permission',{},'permission'),('sha256','0'*64,'size/hash')]:
                with self.subTest(field=field):
                    altered={**config,'audio':{case:{**entry,field:value}}};registry.write_text(json.dumps(altered))
                    with self.assertRaisesRegex(ValueError,reason):builder.load_audio([case],root)
            registry.write_text(json.dumps({**config,'audio':{'Unregistered':entry}}))
            with self.assertRaisesRegex(ValueError,'registered case'):builder.load_audio([case],root)
            registry.write_text(json.dumps(config));target=root/'outside.m4a';source.rename(target);source.symlink_to(target)
            with self.assertRaisesRegex(ValueError,'regular authorized'):builder.load_audio([case],root)


if __name__ == '__main__':
    unittest.main()
