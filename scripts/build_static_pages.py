"""Build only explicitly registered standalone decks for project Pages or an approved blog fallback."""
from html import escape
import hashlib
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


def load_audio(cases, root=ROOT):
    config = json.loads((root / '.github/static-pages.json').read_text())
    audio = config.get('audio', {})
    if not isinstance(audio, dict) or set(audio) - set(cases):
        raise ValueError('Audio must belong to an explicitly registered case')
    approved = {}
    for case, entry in audio.items():
        expected = f'public-audio/{case}.m4a'
        if not isinstance(entry, dict) or entry.get('file') != expected:
            raise ValueError('Audio must use its exact approved public-audio path')
        permission = entry.get('permission', {})
        if not isinstance(permission, dict) or permission.get('status') != 'user-confirmed' or not permission.get('date') or permission.get('record') != 'docs/user-instructions.md':
            raise ValueError(f'Missing public audio permission record for {case}')
        source = root / expected
        if source.parent.is_symlink() or source.is_symlink() or not source.is_file():
            raise ValueError(f'Missing regular authorized audio file for {case}')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if entry.get('sha256') != digest or entry.get('bytes') != source.stat().st_size:
            raise ValueError(f'Authorized audio size/hash mismatch for {case}')
        with source.open('rb') as stream:
            if stream.read(8)[4:8] != b'ftyp':
                raise ValueError(f'Expected an M4A container for {case}')
        approved[case] = (source, f'narration-{digest[:12]}.m4a')
    return approved


def build_site(output=None, root=ROOT, include_audio=True):
    cases = load_cases(root)
    approved_audio = load_audio(cases, root) if include_audio else {}
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
        if case in approved_audio:
            name = approved_audio[case][1]
            html = html.replace(audio, f'<audio id="narration" src="{name}" data-public-audio="true" preload="metadata">')
        else:
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
        if case in approved_audio:
            source, name = approved_audio[case]
            shutil.copyfile(source, dest / name)
        links.append(f'<li><a href="{case}/">{escape(data["title"])}</a><p>{escape(data["author"])} · {len(data["slides"])} 页交互演示</p></li>')
    (output / 'index.html').write_text('''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>视频讲解与交互演示</title><style>body{font:16px system-ui;max-width:880px;margin:60px auto;padding:0 24px;background:#f7f7f4;color:#202a36}h1{font-size:30px}ul{padding:0;list-style:none}li{background:white;padding:24px;margin:24px 0;border:1px solid #ddd;border-radius:12px}a{color:#2456a6;font-size:20px;line-height:1.6}p{line-height:1.7;color:#596473}</style>
<h1>视频讲解与交互演示</h1><p>将视频中的讲解整理为可自由翻页的演示，配有逐页讲稿和原视频来源。</p><ul>''' + ''.join(links) + '</ul></html>\n')
    print(f'Built {len(pages)} registered deck(s): {output}')
    return output


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--without-audio', action='store_true', help='Export HTML-only fallback without public narration')
    parser.add_argument('--output', type=Path, help='Override output directory')
    args = parser.parse_args()
    build_site(output=args.output, include_audio=not args.without_audio)
