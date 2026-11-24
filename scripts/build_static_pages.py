"""Build only explicitly registered standalone decks for the blog's /ai-video-reverse/."""
from html import escape
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_cases(root=ROOT):
    config = json.loads((root / '.github/static-pages.json').read_text())
    cases = config.get('cases')
    if config.get('schema') != 1 or not isinstance(cases, list) or not cases:
        raise ValueError('Register at least one case in .github/static-pages.json')
    if any(not isinstance(case, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', case) for case in cases):
        raise ValueError('Invalid case identifier')
    if len(set(cases)) != len(cases):
        raise ValueError('Duplicate published case')
    return cases


def build_site(output=None, root=ROOT):
    cases = load_cases(root)
    output = Path(output) if output is not None else root / 'dist'
    # Validate and rebuild before replacing the disposable output directory.
    pages = []
    for case in cases:
        presentation = root / 'cases' / case / 'interactive-slides'
        if presentation.is_symlink() or not presentation.is_dir():
            raise ValueError(f'Missing regular presentation directory for {case}')
        subprocess.run([sys.executable, str(root / 'scripts/build_slides.py'), '--case', case], check=True)
        subprocess.run([sys.executable, str(root / 'scripts/validate_case.py'), '--case', case], check=True)
        data = json.loads((presentation / 'slides-data.json').read_text())
        html = (presentation / 'index.html').read_text()
        audio = '<audio id="narration" src="narration.m4a" preload="metadata">'
        if html.count(audio) != 1:
            raise ValueError('Unexpected narration markup; review the online audio policy')
        html = html.replace(audio, '<audio id="narration" data-local-only="true" preload="none">')
        pages.append((case, data, html))
    if output.is_symlink():
        raise ValueError('Output directory must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    links = []
    for case, data, html in pages:
        dest = output / case
        dest.mkdir()
        (dest / 'index.html').write_text(html)
        links.append(f'<li><a href="{case}/">{escape(data["title"])}</a><p>{escape(data["author"])} · {len(data["slides"])} 页交互演示</p></li>')
    (output / 'index.html').write_text('''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>视频讲解与交互演示</title><style>body{font:16px system-ui;max-width:880px;margin:60px auto;padding:0 24px;background:#f7f7f4;color:#202a36}h1{font-size:30px}ul{padding:0;list-style:none}li{background:white;padding:24px;margin:24px 0;border:1px solid #ddd;border-radius:12px}a{color:#2456a6;font-size:20px;line-height:1.6}p{line-height:1.7;color:#596473}</style>
<h1>视频讲解与交互演示</h1><p>将视频中的讲解整理为可自由翻页的演示，配有逐页讲稿和原视频来源。</p><ul>''' + ''.join(links) + '</ul></html>\n')
    print(f'Built {len(pages)} registered deck(s): {output}')
    return output


if __name__ == '__main__':
    build_site()
