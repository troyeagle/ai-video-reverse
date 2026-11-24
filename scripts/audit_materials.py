"""Build source-bound audit datasets and faithful, editable video decks."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HIGH=[('上海',34203,31.4),('北京',30645,44.4),('天津',16301,62.8),('浙江',13230,45.4),('内蒙古',12659,57.8),('江苏',12028,49.9),('广东',10841,50.6),('新疆',10090,64.0),('山西',9400,60.5),('福建',8887,47.9),('重庆',8585,69.8),('海南',8566,58.7),('陕西',8357,63.4),('山东',7831,50.0)]
LOW=[('湖北',7247,56.2),('辽宁',7065,58.1),('四川',7032,56.0),('江西',6882,77.5),('安徽',6836,54.5),('河北',5981,53.3),('吉林',5878,67.4),('贵州',5764,64.0),('湖南',5403,61.0),('黑龙江',5115,68.2),('云南',4831,67.6),('河南',4615,58.8),('甘肃',4554,57.6),('广西',3853,68.6)]
BLOCKS={'names':['A 财力造血','B 收支平衡','C 负债挤压','D 流动性'],'weights':[35,30,25,10],'all':[37.3,61.5,83.9,57.8],'high':[35.6,54.0,79.4,61.2],'low':[39.0,68.9,88.4,56.1]}
HEADROOM=[('广东',.86),('河北',3.13),('山东',3.93),('吉林',3.96),('浙江',4.08),('福建',4.36),('海南',4.60),('江西',4.89),('广西',4.90),('新疆',5.00)]

def check(id,status,title,claim,evidence,times,sources=(),calc='',scope=''):
    return dict(id=id,status=status,title=title,claim=claim,evidence=evidence,times=times,sources=list(sources),calculation=calc,scope=scope)

LFCRI_CHECKS=[
 check('L01','limited','底稿非公开，不能冒充完整原文复算','视频称依据LFCRI分省报告。','用户提供的是首期发布报告的参考文献截图，未包含分省报告正文、表格、子指标阈值与缺失值处理。13项引用只能支持对应公开资料，不能验证全部28省分数。',[0,12,1116,1176],['U1'],scope='来源审计边界'),
 check('L02','limited','报告期与数据截点须区分','片名、页脚写2026年前三季度。','1116秒画面明确写数据截至2026年上半年；1176秒列出各省上半年预算执行和2026H1平台融资。报告发布期不等于数据覆盖期，应注明半年数据，不能说已覆盖三季度省级执行。',[12,1116,1176],['F1','F2','F7'],scope='时点披露'),
 check('L03','issue','低财力组橙区数量：9应核为7','384秒表格标题写“橙区9省”。','按同页14个综合分及60—79分规则，橙区为江西、吉林、贵州、湖南、黑龙江、云南、广西，共7省；另7省黄色。重复出现的同表标题仍写9。',[384,432,516,552],calc='sum(60 ≤ score < 80) = 7',scope='可见表格内部核验'),
 check('L04','issue','最大组间差是B，不是A、C','420秒副标题写“A、C两组差距最大”。','同页显示差值A=3.4、B=14.9、C=9.0、D=5.1。最大为B，第二为C，A最小；副标题与自己的图值不符。',[420],calc='|low − high| = [3.4, 14.9, 9.0, 5.1]'),
 check('L05','issue','D组间差不是15分以上','216秒页底写“B、D两极分化：相差15分以上”。','B差14.9约15，D差只有5.1。D的“15分以上”无法由所列数值支持。',[216,228],calc='61.2 − 56.1 = 5.1'),
 check('L06','limited','D总体均值的样本口径未闭合','216秒总体D均值57.8，两组为61.2和56.1。','按图标28省、两组各14，相同样本下应为58.65；但片尾又列15省融资统计。若实际D样本是高组5省、低组10省，加权恰为57.8。这只是可能解释，不是对底稿样本的认定；需要披露各板实际样本数，不能直接断言57.8算错。',[216,228,396,420],calc='(14×61.2 + 14×56.1) / 28 = 58.65'),
 check('L07','limited','固定权重演算与样本、缺项规则需补齐','权重35%、30%、25%、10%，总体板块均值37.3、61.5、83.9、57.8，综合均值58.0。','若28省都用这组固定板块权重，则均值应服从线性加权，得到58.26。高财力组同样按图列板块得54.63，表内综合分均值约54.04。缺项、不同样本或变权规则可能改变结果；原文未提供，不能将条件演算认定为真实LFCRI数值错误。',[120,132,216,348,420],calc='37.3×.35 + 61.5×.30 + 83.9×.25 + 57.8×.10 = 58.26',scope='条件：同样本、固定板块权重；需底稿解释差异'),
 check('L08','issue','散点纵坐标与数值标签失配','576秒吉林标847%，云南标817%。','按图中200/400/600/800刻度读图，吉林点约在750%，云南点约在720%，偏差接近100个百分点。读图值为近似，但远超数值取整或像素误差。',[576,588,600,612],calc='吉林：标签847，对应位置约750；云南：标签817，对应位置约720',scope='图内标签与坐标核验；不验证真实省级债务比'),
 check('L09','issue','散点上海、天津位置与片内别页数字不符','散点上海约73%/250%，天津约60%/800%。','片内明确上海自给率约93%、债务比约122%；天津82.69%、679.6%。图点不是这些指标的位置。校核视图只使用本片明确数字，不补造其余省份。',[576,660,792],calc='校核点：上海(93,122)，天津(82.69,679.6)'),
 check('L10','issue','“负债端全面橙区”与分区规则不符','216秒标题称负债端全面落在橙区，C均值83.9。','同片定义80—100为红区，83.9应属红区；且上海C=46.3，不能把所有省都称橙区。可以说负债压力普遍较高，不能说全体同一分区。',[132,156,216,240],calc='83.9 ≥ 80；上海46.3 ∈ [40,60)'),
 check('L11','issue','四省病理图的概述与柱值失配','996秒称吉林A/B/C“全线危重高压”。','同图吉林A=47、B=32、C=92；按片内规则分别黄、绿、红。B=32与“全线危重”不符。原图D部分标“无”，不能补成0。',[996,1056],calc='吉林 A/B/C = 47/32/92 → 黄/绿/红'),
 check('L12','inference','额度空间不是永久举债能力','多页把低剩余额度推至“彻底失去继续扩张负债能力”。','余额/限额是特定时点的约束，预算新增额度、结存额度安排和转移支付会改变约束。截图引用的2026预算及10月5500亿元结存限额文件本身包含动态政策。不能据此直接预测永久没有融资途径。',[276,300,936,948],['F5','F9'],scope='条件性政策推论'),
 check('L13','limited','28省合计不能直接当作全国三季度数','口述将28省余额53.99、限额57.10描述为全国约束。','视频剔除西藏、青海、宁夏；F7是全国8月余额59.8955万亿元，F5是2026全年法定限额63.18743万亿元。样本和时点不同，不能互相直接替代或据不相等判原数据虚假。',[276,312,1176],['F5','F7'],calc='(188689.22 + 443185.08) / 10000 = 63.18743万亿元'),
 check('L14','limited','口述极差21.3须回听原音','387.9秒转写记21.3，546.96秒记24.2。','可见低组表最大77.5、最小53.3，极差24.2。这里标为转写/原音待确认，不以单次ASR确定作者口误；原视频与转写错误必须区分。',[384,388,547,552],calc='77.5 − 53.3 = 24.2',scope='待原音听核'),
 check('L15','inference','改善被称“虚假复苏”需额外依据','636秒山西、内蒙古卡片标题称虚假复苏。','可见数据说明A/B修复与C存量压力并存，不足以证明改善完全虚假或只由资源价格推动。需要省级收入结构、价格和底稿分解证据；本次材料未补齐。',[624,636],['F3','F13']),
 check('L16','limited','缺项与“可算省份”列解释不足','120秒表可算省份写1/2/1/1，1116秒称12项只有4项全省算全。','未披露每个缺失指标的代理、重标权重和统一评分阈值。不能仅凭有12项/35-30-25-10权重就复算或认可28省可比性。',[120,1116,1176]),
 check('P01','pass','28省总体分区与极差可对上','总体1绿、15黄、12橙、0红，极差46.1。','按视频两张14省表的显示值，分区计数、最大江西77.5和最小上海31.4一致。',[168,180,348,384],calc='77.5 − 31.4 = 46.1；分区计数1/15/12/0'),
 check('P02','pass','8.01分可以复算，不能误判','两组差由5.55扩大至8.01。','从14+14省表计算，高组均值54.042857、低组62.057143，差8.014286约8.01；只拿已取整54.0和62.1相减会造成误判。',[348,384,528],calc='62.057143 − 54.042857 = 8.014286 ≈ 8.01'),
 check('P03','pass','5.4%剩余额度算术成立','图中余额53.99、限额57.10、剩余3.11万亿元。','使用该图自己的精确显示值可以得到约5.4%。此核验不证明28省原始数据真实或可代表全国。',[276,288],calc='(57.10 − 53.99) / 57.10 ×100 = 5.4466% ≈ 5.4%'),
 check('P04','pass','9省小于5%，新疆是参照项','图中10个柱，文字写九省低于5%。','显示值中前9省严格小于5，新疆等于5.00，应作为阈值参照；10根柱不等于文案计数错误。',[276],calc='count(headroom < 5.00) = 9'),
 check('P05','pass','“指数不是评级”边界值得保留','六条判断及边界页声明排序不构成偿债能力评级。','复原网页保留这一约束，不把分数解释成违约概率或官方评级。',[48,156,1116]),
]

LFCRI_CHECKS.extend([
 check('L17','inference','比率改善不能直接证明公共服务存量耗损','天津卡片称支出缩减导致虚假的自给率改善并消耗公共服务存量。','支出增速与自给率可以说明流量或分母变化，不能单独证明服务质量、资产或存量耗损；本次资料没有补齐这项结果证据。',[792,1080],['F5']),
 check('L18','issue','A板块低风险分不能读成造血能力弱','216秒脚注说A均值37.3说明造血能力整体偏弱。','本片定义指数越高压力越大，A37.3是相对较低的压力分，并非低能力评分；不能反读成造血能力弱，也不能反过来仅据此证明绝对财力强。',[216,228],calc='压力分37.3 < 40；能力强弱与风险分方向须分清')
])

QS_CHECKS=[
 check('Q01','pass','三期及文章对应关系成立','9月中旬至10月中旬，连续三期同主题。','求是网原文确为2026/18、19、20期，发布时间9月16日、10月1日、10月16日；作者均为本刊评论员。',[0,12,48,108,312],['S1','S2','S3']),
 check('Q02','pass','供需相对错配与供给优势主线有依据','需求增长未同步跟上供给扩张和升级。','S1讨论有效需求扩张相对滞后，并强调供给体系和市场优势；S2解释阶段与模式转变中的错配、梗阻。',[48,60,72,108,156],['S1','S2']),
 check('Q03','pass','收入分配、社保与消费机制对应原文','收入分配、社会保障影响消费能力和意愿。','S2明确论述收入分配制度和社会保障制约消费，强调就业、收入预期与长效机制。',[168,180,204,216,252],['S2']),
 check('Q04','pass','消费税改革与地方激励的联系有依据','后移征收环节、下划地方，改变重生产轻消费取向。','S2确实提出该改革并将其与资源配置从重生产轻消费向平衡发展联系；视频使用未来条件，没有宣称已全部落地。',[264,276,288,300],['S2']),
 check('Q05','pass','四环节与四种协同对应第三文','生产、分配、流通、消费；财政金融等协同。','S3按四环节分析，并分别讨论财政金融、宏观政策与改革、发展与民生、实施与预期协同。',[312,324,336,348,372,384],['S3']),
 check('Q06','inference','“原文是”实际为忠实转述','167.86秒及画面标“原文”的句子。','意思与S2一致，但将原文“明显向生产领域倾斜”“受到较大制约”等改写为“更多”“影响”。宜标“原文要旨/转述”，不能当逐字引文。',[168],['S2'],scope='引述规范，非实质歪曲'),
 check('Q07','inference','总结偏向消费，投资分量被压缩','最终重点为居民收入、社保和消费激励。','S1强调投资潜力和补短板；S2/S3也强调有效投资、民间投资及重大工程。视频的总结可成立为作者选取的主线，但不是三文完整政策清单。',[84,120,252,396,420,456],['S1','S2','S3']),
 check('Q08','inference','房地产资产负债表为作者推演','369.62秒举房地产继续压制家庭资产负债表。','S3谈就业收入预期和家庭负担，并未给出这个具体房地产传导例子。将其作为作者举例而不是求是直接表述。',[360,372],['S3']),
 check('Q09','inference','“不能压缩生产”应保留限定','结尾说不能靠压缩生产能力解决需求不足。','原文保留供给优势，也要求优质供给、市场出清和兼并整合。视频此前也提淘汰低效供给，应避免读成所有存量产能均不得退出。',[84,396,432,456],['S1','S2']),
 check('Q10','limited','“极为少见”没有频次证明','一个月连续三期被称极为少见。','三期事实成立，稀有程度需历史刊发统计；三篇原文自身不能证明此判断。',[0,12],['S1','S2','S3']),
 check('Q11','limited','“去年刚提出投资于人”不是三文可证明的历史结论','209.7秒谈去年刚提出投资于人。','三篇原文使用该概念，但没有交代首次提出史；本次将这一句归为需另查历史出处的外延表述，不据此判定真假。',[204,216],['S1','S2','S3']),
]

LF_PHASES=[(0,'cover','地方财政危机指数：深度诊断'),(12,'summary','LFCRI分省评估：28省同一标尺'),(24,'questions','这份解读回答三个问题'),(36,'summary','总量得分掩盖了具体病灶'),(48,'summary','先给结论：六条判断'),(60,'ranking','28省财政压力排序'),(84,'change','一年间的分值变化'),(96,'jiangsu','江苏：财力强省的流动性陷阱'),(108,'section','01 · 怎样衡量财政压力'),(120,'model','四个板块，十二项指标'),(132,'weights','四本账与四个风险板块'),(156,'boundary','分级与三条禁忌'),(168,'distribution','均值58.0：分布比水平更重要'),(180,'ranking','28省财政压力排序'),(216,'means','四个板块里，只有负债端全面落在橙区'),(240,'means','财政健康仪表盘：板块分布'),(276,'headroom','债务限额余量与九省阈值'),(300,'headroom','限额之墙：扩张约束'),(312,'grouping','为什么必须分组看'),(324,'weights','四本账：收入、平衡、负债与流动性'),(336,'grouping','体量不等于能力'),(348,'high','高财力组：14省，上海独在绿区'),(360,'high-story','高财力组的内部差异'),(384,'low','低财力组：橙区9省，压力最集中'),(396,'comparison','高、低财力组的结构差异'),(408,'low-story','低财力组：收入、负债与融资三条线'),(420,'comparison','同一板块，两组相差15分'),(432,'low','低财力组分值表'),(444,'comparison','财力与压力：四板块对比'),(516,'low','低财力组分值表'),(528,'trend','一年间：两组差距5.55到8.01'),(552,'low','分化扩大后的低财力组'),(564,'summary','总分与结构：最终判断'),(576,'scatter','自给率与债务收入比'),(624,'change','改善、恶化与被掩盖'),(636,'shanxi','山西与内蒙古：虚假的复苏'),(660,'shanghai','安徽与上海：不同改善机制'),(708,'jilin','收入进度掉队，债务已到顶'),(720,'jilin','吉林：高基数与负债约束'),(780,'tianjin','天津：收入不弱，额度吃紧'),(792,'tianjin','天津：分母收缩的纸面幻觉'),(852,'jiangsu','城投融资转负：流动性先出问题'),(864,'jiangsu','江苏：冰山上下的不同压力'),(900,'locked','云南与贵州：存量锁定'),(912,'locked','云南与贵州：缺乏弹性的债务账本'),(936,'guangdong','广东、浙江：分数尚可，压力犹存'),(948,'guangdong','广东、浙江：额度与收入的对照'),(996,'patients','同样总分，完全不同的病理'),(1008,'high','回看高财力组分值表'),(1020,'section','04 · 六条结论与数据边界'),(1032,'summary','结构性压力：六条判断'),(1056,'patients','四省病理与指标分值'),(1068,'headroom','回看限额之墙'),(1080,'tianjin','回看天津：分母效应'),(1092,'typology','财政风险的四种病理'),(1116,'boundary','三条边界：方法、口径与时点'),(1128,'blind','模型未计入的隐患'),(1164,'summary','总量之外的结构风险'),(1176,'sources','数据来源与口径')]
QS_PHASES=[(0,'cover','《求是》三文：供强需弱'),(12,'timeline','9月中旬—10月中旬：三期同题'),(24,'quote','只看消费偏弱，解释还不够'),(36,'quote','过去几十年的增长模式，怎样调整'),(48,'article','第一篇：立足优势'),(60,'two','承认矛盾，同时保留供给优势'),(72,'quote','需求没有同步跟上供给扩张'),(84,'two','不同判断，导向不同政策'),(108,'article','第二篇：以改革发力'),(120,'flow','从短缺出发的生产体系'),(144,'flow','地方政府与生产端的资源配置'),(156,'two','工业体系与制造能力'),(168,'quote','资源配置、收入分配与社会保障'),(180,'quote','收入在政府、企业、居民间怎样分配'),(204,'flow','家庭的未来支出与储蓄选择'),(216,'quote','投资于人：社会保障与消费预期'),(228,'two','今天的购买力与未来的安全感'),(252,'quote','从消费政策进入收入、财政与社会政策'),(264,'tax','消费税改革与地方激励'),(288,'tax','让地方更关心收入、服务与消费'),(312,'article','第三篇：以政策协同'),(324,'cycle','生产、分配、流通、消费'),(348,'quote','无法靠一个政策独自解决'),(360,'two','几个政策失配的例子'),(384,'policy','财政金融、改革、民生与预期协同'),(396,'two','保留优势，同时改变增长依赖'),(420,'policy','建立更强的需求形成机制'),(432,'quote','让市场淘汰低效供给'),(444,'quote','增长模式的再平衡'),(456,'conclusion','两端共同调整：供给与需求')]

def fix(text,case):
    shared={'共强虚弱':'供强需弱','供强虚弱':'供强需弱','工强虚弱':'供强需弱','扣问':'叩问','获章':'扩张','需求形成旗帜':'需求形成机制','下滑地方':'下划地方'}
    local={'自己率':'自给率','城区':'橙区','财力造学':'财力造血','财力造险':'财力造血','财力造写':'财力造血','收值平衡':'收支平衡','借薪还救':'借新还旧','做税':'作祟','所有成分':'所有省份','税机':'税基','飞标':'非标','长付的节奏':'偿付的节奏','土地出厂':'土地出让','复息':'付息','滚序':'滚续','低板块':'D板块','96.7%':'96.7分','27.4%':'27.4分'} if case=='BV11ts56mEVt' else {}
    for a,b in (shared|local).items():text=text.replace(a,b)
    return text.replace(',','，').replace('?','？').strip()

def build(case_id,phases,checks):
    case=ROOT/'cases'/case_id
    metadata=json.loads((case/'video-info.json').read_text())
    raw=json.loads((case/'转写草稿.json').read_text())
    duration=raw['duration']
    words=[w for s in raw['segments'] for w in s['words'] if w['start']<duration and w['word'].strip()]
    sources=[]
    if case_id=='BV1JXxB6rErv':
        titles=['立足优势着力破解供强需弱矛盾','以改革发力破解供强需弱矛盾','以政策协同破解供强需弱矛盾']
        dates=['2026-09-16','2026-10-01','2026-10-16']
        rows=json.loads((case/'sources/retrieval.json').read_text())
        for i,row in enumerate(rows):sources.append(dict(id=row['id'],title=titles[i],date=dates[i],publisher='《求是》杂志评论员',url=row['url'],status='官方原文已读取',issue=f'2026/{18+i}'))
    else:
        sources.append(dict(id='U1',title='LFCRI报告及参考文献页',publisher='用户告知报告非公开',url=None,status='只有参考文献截图，无分省底稿正文；原图仅本地保存'))
        for row in json.loads((case/'sources/reference-retrieval.json').read_text()):
            preview=row.get('preview','').split('\n')[0]
            sources.append(dict(id=row['id'],title=preview if preview and preview!='PDF' else ('标普信用评级：2026城投中期回顾' if row['id']=='F13' else row['id']+'（截图引用）'),url=row['url'],publisher='截图引用的公开出处',status='访问失败，不能据此判来源不存在' if row.get('error') else ('仅核验公开题名/摘要，未越过付费限制' if row['id'] in ['F10','F11'] else '公开原文已取得')))
    utterances=[];group=[]
    for index,w in enumerate(words):
        group.append(w)
        text=''.join(x['word'] for x in group)
        final=w['word'].endswith(('。','？','?','！','!'))
        comma=w['word'].endswith((',', '，','；',';')) and (len(text)>=45 or w['end']-group[0]['start']>=10)
        pause=index+1<len(words) and words[index+1]['start']-w['end']>.6 and len(text)>8
        if final or comma or pause:
            a=group[0]['start'];b=min(duration,group[-1]['end'])
            utterances.append(dict(start=a,end=max(b,a+.001),text=fix(text,case_id)));group=[]
    if group:utterances.append(dict(start=group[0]['start'],end=min(duration,group[-1]['end']),text=fix(''.join(w['word'] for w in group),case_id)))
    originals={
        'high':'高财力组：14省里，只有上海在绿区',
        'low':'低财力组：橙区9省，压力最集中',
        'weights':'四本账：四个风险板块',
        'grouping':'为什么必须分组看：体量不等于能力',
        'patients':'同样的总分，完全不同的病理',
    }
    scene_names={'cover':'封面','summary':'结构判断','questions':'三个问题','section':'章节分隔','ranking':'省份排序','model':'指标构成','weights':'权重','boundary':'使用边界','distribution':'总体分布','means':'板块均值','headroom':'限额余量','grouping':'分组口径','high':'高财力组表','high-story':'高组结构','low':'低财力组表','low-story':'低组结构','comparison':'板块对照','trend':'同比变化','change':'变化类型','scatter':'双指标分布','shanxi':'山西与内蒙古','shanghai':'安徽与上海','jilin':'吉林','tianjin':'天津','jiangsu':'江苏','locked':'云南与贵州','guangdong':'广东与浙江','typology':'风险类型','blind':'未量化部分','sources':'来源','timeline':'刊期','article':'文章要旨','quote':'关键论断','two':'两种机制','flow':'机制演示','cycle':'经济循环','policy':'政策协同','tax':'消费税改革','conclusion':'总结'}
    slides=[]
    for i,(start,scene,title) in enumerate(phases):
        end=phases[i+1][0] if i+1<len(phases) else duration
        cues=[c for c in utterances if start<=(c['start']+c['end'])/2<end]
        if case_id=='BV11ts56mEVt' and scene in originals:title=originals[scene]
        dark=case_id=='BV11ts56mEVt' and scene not in ['questions','model','boundary','distribution','grouping','high','high-story','low','low-story','trend','sources','section'] and start not in [12,48,276,420,624,708,780,852,900,936,1032,1116,1176]
        audit_ids=[c['id'] for c in checks if any(start<=t<end for t in c['times'])]
        has_words=any(start<=(w['start']+w['end'])/2<end for w in words)
        reason=('短转场的口播句跨页，请结合前后页讲稿与原声。' if has_words else '此资料画面没有新增口播。') if not cues else ''
        slides.append(dict(id=i+1,start=start,end=end,title=title,phaseName=scene_names.get(scene,title)+' · '+f'{int(start)//60:02}:{int(start)%60:02}',scene=scene,theme='dark' if dark else ('editorial' if case_id=='BV1JXxB6rErv' else 'paper'),source='按可见元素重绘；数据与原文边界见审计',timeLabel=f'{int(start)//60:02}:{int(start)%60:02}—{int(end)//60:02}:{int(end)%60:02}',cues=cues,auditIds=audit_ids,narration_free=not cues,empty_reason=reason))
    if case_id=='BV1JXxB6rErv':
        excerpts=[[('S1p2','正文第2自然段','国内有效需求扩张速度总体相对滞后'),('S1p4','正文第4自然段','投资增长的潜力依然巨大')],[('S2p3','正文第3自然段','资源配置和政策取向明显向生产领域倾斜'),('S2p5','正文第5自然段','推进消费税征收环节后移并稳步下划地方')],[('S3p2a','正文第2自然段','不可能单靠某一方面某一领域的政策加以解决'),('S3p2b','正文第2自然段','把生产发展、分配改善、流通畅通和消费扩大贯通起来')]]
        for source,items in zip(sources,excerpts):
            source['excerpts']=[dict(id=k,location=loc,text=t) for k,loc,t in items]
            assert sum(len(x['text']) for x in source['excerpts'])<=90
    data=dict(title=metadata['title'],author=metadata['owner']['name'],source='https://www.bilibili.com/video/'+case_id+'/',caseId=case_id,duration=duration,slides=slides,data=dict(high=HIGH,low=LOW,blocks=BLOCKS,headroom=HEADROOM) if case_id=='BV11ts56mEVt' else {},audit=dict(summary='内部图表审计与公开引用核验；非公开底稿未提供，不能认证LFCRI原始评分' if case_id=='BV11ts56mEVt' else '求是三篇原文对照：区分忠实转述、作者推演及待补证表述',findings=checks,sources=sources),timing_note='按12秒高清采样识别可见阶段，起点为采样近似；审计证据指向准确的原视频帧时刻。')
    p=case/'interactive-slides';p.mkdir(exist_ok=True)
    (p/'slides-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    calibrated=dict(source=data['source'],method='逐字时间拆分与画面术语校订；未将审计建议替换到原讲稿',duration=duration,segments=[c for s in slides for c in s['cues']])
    normalized=lambda t: ''.join(c for c in t if c.isalnum())
    assert normalized(fix(''.join(w['word'] for w in words),case_id)) == normalized(''.join(c['text'] for c in calibrated['segments'])), 'Words lost or correction split across page boundaries'
    (case/'校订转写.json').write_text(json.dumps(calibrated,ensure_ascii=False,indent=2))
    (case/'校订转写.txt').write_text('\n'.join(c['text'] for c in calibrated['segments'])+'\n')
    (case/'audit.json').write_text(json.dumps(data['audit'],ensure_ascii=False,indent=2))
    (case/'README.md').write_text(f'# {data["title"]}\n\n原视频：{data["source"]}\n\n作者：{data["author"]}；时长{duration:.2f}秒；{len(slides)}个可选择画面阶段。\n\n- [交互演示](interactive-slides/index.html)\n- [审计报告](审计报告.md)\n- [校订讲稿](视频讲稿.md)\n\n{data["audit"]["summary"]}。\n\n{data["timing_note"]}\n\n截图只作证据；图形由CSS/SVG绘制。网页的校核对照不是底稿认证；未披露的分省数据不补造。\n')
    (case/'视频讲稿.md').write_text('# '+data['title']+'\n\n根据原声转写并校订术语，保留作者观点；审计结论另列。对话如有多人，不凭句式强行指定说话人；保留可回听的原句。\n\n'+ '\n\n'.join('### '+s['timeLabel']+' · '+s['title']+'\n\n'+''.join(c['text'] for c in s['cues']) for s in slides))
    report=['# '+data['title']+'：原视频审计\n',data['audit']['summary']+'。\n\n证据分为原视频画面/原声、提供的材料与可独立核验的公开原文；“核验通过”只指指定范围，不代表对所有经济事实或LFCRI模型有效性背书。\n\n校核视图明确标示修正依据，不悄悄改写原视频讲稿。\n']
    statuses={'issue':'确认的内部不一致','limited':'证据不足/范围限制','inference':'作者推演或表述边界','pass':'核验一致（限定范围）'}
    for c in checks:
        t=c['times'][0]
        report.append(f'## {c["id"]} · {c["title"]}\n\n判定：**{statuses[c["status"]]}**\n\n原视频表述：{c["claim"]}\n\n核验依据：{c["evidence"]}\n\n'+(f'演算：`{c["calculation"]}`\n\n' if c['calculation'] else '')+f'[原视频 {t} 秒]({data["source"]}?t={t}) · [本地证据帧](evidence/frames/{int(t)//12*12:04}.jpg)\n\n'+(f'适用范围：{c["scope"]}\n\n' if c['scope'] else ''))
    report.append('## 来源清单\n\n')
    for s in sources:report.append(f'- {s["id"]} · {s["title"]} · {s["status"]}'+(f' · {s["url"]}' if s['url'] else '')+'\n')
    report.append('\n## 校订与方法说明\n\n原始ASR保存在语音识别.json。只校订明显同音错字及据画面的术语，疑似口误没有按期望结论改写；L14保留为原音待听核。96.7/27.4的单位据画面校订为分，不把ASR的百分号当作确定的视频错误。来源原文与用户截图位于sources/raw，仅本地保存，不进入网页发布包。\n')
    if case_id=='BV1JXxB6rErv':
        report.append('\n## 原文短引定位\n\n正文自然段从第一段正文计数，以下短引只用于定位与对照。\n')
        for source in sources:
            for excerpt in source.get('excerpts',[]):
                report.append(source['id']+' · '+excerpt['location']+'：'+excerpt['text']+'\n')
    (case/'审计报告.md').write_text('\n'.join(report))
    print(case_id,len(slides),'slides',len(calibrated['segments']),'cues',len(checks),'audit entries')

if __name__=='__main__':
    build('BV11ts56mEVt',LF_PHASES,LFCRI_CHECKS)
    build('BV1JXxB6rErv',QS_PHASES,QS_CHECKS)
