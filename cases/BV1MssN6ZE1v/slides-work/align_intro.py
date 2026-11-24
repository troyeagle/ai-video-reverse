import os,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
os.environ['HF_HOME']=str(root/'.model-cache')
os.environ['XDG_CACHE_HOME']=str(root/'.runtime-cache')
import mlx_whisper
result=mlx_whisper.transcribe(str(root/'slides-work'/'intro.wav'),path_or_hf_repo='mlx-community/whisper-large-v3-turbo',language='zh',word_timestamps=True,verbose=False,initial_prompt='Alpha茶水间，离岸信托，财政资金，高盛，社保征缴，5000亿元，2.8万亿元，2.3万亿元，4.1万亿元。')
(root/'slides-work'/'intro-aligned.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('Intro alignment complete')
