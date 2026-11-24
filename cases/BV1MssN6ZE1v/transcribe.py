import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ['HF_HOME'] = str(ROOT / '.model-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / '.runtime-cache')
os.environ['MPLCONFIGDIR'] = str(ROOT / '.runtime-cache' / 'matplotlib')

import mlx_whisper

started = time.time()
print('Starting Chinese transcription with Whisper large v3 turbo', flush=True)
result = mlx_whisper.transcribe(
    str(ROOT / 'audio.m4s'),
    path_or_hf_repo='mlx-community/whisper-large-v3-turbo',
    language='zh',
    verbose=True,
    condition_on_previous_text=True,
    initial_prompt='这是Alpha茶水间关于财政、税收、社保、土地财政和宏观税负的中文讲解。请使用简体中文和正确标点。',
)
(ROOT / '语音识别.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
(ROOT / '语音识别原文.txt').write_text(result['text'] + '\n')

def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'

(ROOT / '语音识别.srt').write_text('\n\n'.join(
    f'{i}\n{timestamp(s["start"])} --> {timestamp(s["end"])}\n{s["text"].strip()}'
    for i, s in enumerate(result['segments'], 1)
) + '\n')
print(f'Transcription complete in {time.time() - started:.1f} seconds', flush=True)
