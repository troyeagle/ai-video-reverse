"""Transcribe requested cases using the existing local MLX model cache."""
import argparse
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', action='append', required=True)
args = parser.parse_args()
os.environ['HF_HOME'] = str(ROOT / 'cases/BV1MssN6ZE1v/.model-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / '.local/asr-runtime')
import mlx_whisper

def stamp(t):
    ms=round(t*1000); sec,ms=divmod(ms,1000);minute,sec=divmod(sec,60);hour,minute=divmod(minute,60)
    return f'{hour:02}:{minute:02}:{sec:02},{ms:03}'

for case_id in args.case:
    case=ROOT/'cases'/case_id
    duration=float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(case/'原视频.mp4')]))['format']['duration'])
    print(f'Start {case_id}, {duration:.3f}s',flush=True)
    begin=time.time()
    raw=mlx_whisper.transcribe(str(case/'audio.m4s'),path_or_hf_repo='mlx-community/whisper-large-v3-turbo',language='zh',word_timestamps=True,verbose=False,initial_prompt='中文财政与经济政策讨论，使用简体中文。地方财政危机指数 LFCRI，省级财政，供强需弱，《求是》杂志。保留原话、数字和标点。')
    (case/'语音识别.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2))
    (case/'语音识别原文.txt').write_text(raw['text']+'\n')
    segments=[]
    for s in raw['segments']:
        if s['start']>=duration:continue
        text=s['text'].strip().replace(',', '，').replace('?', '？')
        if not text:continue
        segments.append({'start':s['start'],'end':min(duration,s['end']),'text':text,'words':s.get('words',[])})
    payload={'source':'https://www.bilibili.com/video/'+case_id+'/','method':'MLX Whisper large-v3-turbo, word timestamps; automatic draft pending frame-based correction','duration':duration,'segments':segments}
    (case/'转写草稿.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    (case/'转写草稿.txt').write_text('\n'.join(s['text'] for s in segments)+'\n')
    (case/'转写草稿.srt').write_text('\n\n'.join(f'{i}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(segments,1))+'\n')
    print(f'Finished {case_id}: {len(segments)} segments in {time.time()-begin:.1f}s',flush=True)
