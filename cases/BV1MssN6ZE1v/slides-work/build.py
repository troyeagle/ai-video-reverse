import json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DEST=ROOT/'interactive-slides'
DEST.mkdir(exist_ok=True)
pages=[
 (0,'财政的钱，为什么还是不够？','财政缺钱的信号','fiscal',1,''),
 (13.8,'多收的钱，填不满缺口','严查税与强化社保：新增5000亿元','gap',1,'2026年，相比2021年 · 高盛测算'),
 (34.1,'多收的钱，填不满缺口','2.8万亿元缺口，仍差2.3万亿元','gap',2,'2026年，相比2021年 · 高盛测算'),
 (44.4,'多收的钱，填不满缺口','2030年：缺口或至4.1万亿元','gap',3,'2026年，相比2021年 · 高盛测算'),
 (64.1333,'看起来，中国还有加税空间？','中口径税负：中国24.4%，OECD 34.1%','gross',1,'2024年 · CF40研究'),
 (97.3667,'减去返还居民的部分，留下多少？','收走的钱 − 公共社会保障支出','return',1,'2024年 · CF40研究'),
 (111.5,'减去返还居民的部分，留下多少？','实收税负：中国13.9%，OECD 12.9%','net',1,'2024年 · CF40研究'),
 (127.4667,'收入、福利与净负担','人均收入四成多，净负担已追上','income',1,'人均GDP按购买力平价比较'),
 (145.7333,'拿走以后，创造了多少？','基础设施投资与长期回报','infra',1,''),
 (184.0333,'同样的投入，回报正在改变','资本存量增加，投资边际回报下降','returns',1,''),
 (230.5,'想少拿，为什么不容易？','更多收入留给居民与私人部门','rebalance',1,''),
 (235.76,'想少拿，为什么不容易？','债务、养老金和老龄化锁住支出','locked',1,''),
 (271.5667,'土地财政：钱从哪里来？','房地产、银行与地方财政','land',1,''),
 (290.08,'土地财政：钱从哪里来？','家庭储蓄与现金流进入土地体系','land',2,''),
 (312.2667,'收入退潮，账单还在','土地出让收入较高点下降约70%','expense',1,'高盛报告及测算'),
 (323.72,'收入退潮，账单还在','199万亿元债务，6.2万亿元利息','expense',2,'高盛报告及测算'),
 (333.48,'收入退潮，账单还在','财政对社保基金补贴超3万亿元','expense',3,'高盛报告及测算'),
 (359.2333,'先把旧账收干净','没交的开始交，少交的开始补','collect',1,''),
 (374.1,'征管收紧：同一套规则，不同的执行','灵活 → 灰色空间 → 漏洞','rules',1,''),
 (394.8,'征管收紧：同一套规则，不同的执行','应收尽收，实际负担上升','rules',2,''),
 (403.5,'堵住漏洞，也有上限','新增约1万亿 / 年，缺口或至4.1万亿','limits',1,'2030年 · 高盛测算'),
 (436.0667,'负担已经不低，钱还是不够','实收税负13.9%，财政资金仍不足','burden',1,'CF40实收口径'),
 (469.7,'接下来，看税基的边界','让更多的钱进入征税范围','taxbase',1,''),
 (486.8,'接下来，看税基的边界','工资、利润、消费、资本收益与财产','taxbase',2,''),
 (498.22,'接下来，看税基的边界','税收收入增长与未来财产税研究','taxbase',3,''),
 (522.7333,'税率表没动，能征到的部分变多','足额缴纳、优惠减少、范围扩大','static',1,''),
 (541.2,'税率表没动，能征到的部分变多','能留下的钱更少，能被征到的钱更多','static',2,''),
 (557.7333,'财政收入的来源，正在改变','过去：土地、房地产、平台与债务','oldsource',1,''),
 (565.4,'财政收入的来源，正在改变','未来：收入、利润、消费、收益与财产','sources',1,''),
 (578,'土地财政退场，压力寻找新出口','低显性税负模式的基础正在退出','exit',1,''),
 (595.3333,'加税，会以什么名字出现？','征管、实缴、优惠、直接税与财产税','ways',2,''),
 (613.9667,'加税，会以什么名字出现？','严查税和强化社保，更像是序章','ending',2,''),
]
assert len(pages)==32

def normal(text):
    fixes={'事业保障':'失业保障','眨眼':'扎眼','购买力评价':'购买力平价','实手口径':'实收口径','低险性税负':'低显性税负','社保时角':'社保实缴','税机的边界':'税基的边界','难掩下去':'难演下去','征税事业':'征税视野','公司条':'工资条','明义税率':'名义税率','不涨得像税':'不长得像税','把能查的都查了账':'把能查的都查了，账'}
    for a,b in fixes.items():text=text.replace(a,b)
    return text.replace(',','，').replace('?','？').strip()

base=json.loads((ROOT/'校订转写.json').read_text())['segments']
aligned=json.loads((HERE/'intro-aligned.json').read_text())
intro=[]
for seg in aligned['segments']:
    words=seg.get('words',[])
    if not words:continue
    chunk=[]
    for word in words:
        chunk.append(word)
        if re.search(r'[,.?!，。？！]$',word['word']):
            intro.append({'start':chunk[0]['start'],'end':chunk[-1]['end'],'text':normal(''.join(w['word'] for w in chunk))});chunk=[]
    if chunk:intro.append({'start':chunk[0]['start'],'end':chunk[-1]['end'],'text':normal(''.join(w['word'] for w in chunk))})
corpus=intro+[dict(s,text=normal(s['text'])) for s in base if s['start']>=64]
corpus.sort(key=lambda c:c['start'])

def timestamp(t):
    t=int(t);return f'{t//60:02}:{t%60:02}'

slides=[]
for i,(start,title,phase_name,scene,phase,source) in enumerate(pages):
    end=pages[i+1][0] if i+1<len(pages) else 623.92
    cues=[c for c in corpus if start<=(c['start']+c['end'])/2<end]
    merged=[]
    for c in cues:
        if merged and len(merged[-1]['text']+c['text'])<=78 and c['end']-merged[-1]['start']<=10:
            merged[-1]['text']+=c['text'];merged[-1]['end']=c['end']
        else:merged.append(dict(c))
    assert merged, f'Page {i+1} has no cues'
    slides.append({'id':i+1,'start':start,'end':end,'title':title,'phaseName':phase_name,'scene':scene,'phase':phase,'source':source,'timeLabel':f'{timestamp(start)}—{timestamp(end)}','cues':merged})
assert ''.join(c['text'] for c in corpus)==''.join(c['text'] for s in slides for c in s['cues'])
deck={'title':'严查税、补社保只是序章：土地财政退潮后，钱从哪里来？','author':'Alpha茶水间','source':'https://www.bilibili.com/video/BV1MssN6ZE1v','duration':623.92,'slides':slides}
data=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
html=(HERE/'template.html').read_text()
for token,content in [('/*__STYLE__*/',(HERE/'style.css').read_text()),('<!--__ICONS__-->',(HERE/'icons.svg').read_text()),('/*__DATA__*/',data),('/*__RENDER__*/',(HERE/'render.js').read_text()),('/*__APP__*/',(HERE/'app.js').read_text())]:html=html.replace(token,content)
(DEST/'index.html').write_text(html)
(DEST/'slides-data.json').write_text(json.dumps(deck,ensure_ascii=False,indent=2))
(DEST/'页面与讲稿对照.md').write_text('# 页面与原视频讲稿对照\n\n'+ '\n\n'.join(f'## {s["id"]:02} · {s["title"]}\n\n{s["phaseName"]} · 原视频 {s["timeLabel"]}\n\n'+ '\n\n'.join(c['text'] for c in s['cues']) for s in slides))
print(f'Built {len(slides)} slides, {sum(len(s["cues"]) for s in slides)} transcript rows, HTML {len(html.encode()):,} bytes')
print('All source transcript content mapped exactly once.')
