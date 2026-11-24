const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const icon = (name,label='') => `<svg class="pictogram" viewBox="0 0 100 100" ${label?`role="img" aria-label="${esc(label)}"`:'aria-hidden="true"'}><use href="#icon-${name}"/></svg>`;
const F = (html,n=1,style='',extra='') => `<div class="fragment ${extra}" data-order="${n}" style="${style}">${html}</div>`;
const at = (html,x,y,n=1,extra='') => F(html,n,`position:absolute;left:${x}px;top:${y}px`,extra);
const plinth = '<svg class="plinth" viewBox="0 0 160 65" aria-hidden="true"><ellipse cx="80" cy="57" rx="69" ry="7"/><polygon class="top" points="0,21 75,0 160,24 84,48"/><polygon class="side" points="84,48 160,24 160,42 84,65"/><polygon class="front" points="0,21 84,48 84,65 0,39"/></svg>';
function figure(name,label,x,y,size=82,platform=false,n=1,extra='') {return F(`${platform?plinth:''}${icon(name,label)}${label?`<div class="scene-label">${esc(label)}</div>`:''}`,n,`left:${x}px;top:${y}px;--size:${size}px`, `figure ${platform?'on-platform':''} ${extra}`);}
function floatIcon(name,x,y,size,n=1){return F(icon(name),n,`left:${x}px;top:${y}px;width:${size}px;height:${size}px`,'float-icon');}
function coinGroup(x,y,count=3,n=2){let s='';for(let i=0;i<count;i++)s+=`<span class="money-coin" style="left:${(i%3)*29}px;top:${Math.floor(i/3)*29}px">${icon('coin')}</span>`;return at(s,x,y,n);}
let flowSerial=0;
function flow(paths,n=1,animate=true){let s='';for(const d of paths){const id=`line-${++flowSerial}`;s+=`<path id="${id}" d="${d}" class="flow-path draw"/>`;if(animate)s+=`<circle r="3" class="moving-coin"><animateMotion dur="4.8s" repeatCount="indefinite"><mpath href="#${id}"/></animateMotion></circle><circle r="2.3" class="moving-coin"><animateMotion dur="4.8s" begin="-2.5s" repeatCount="indefinite"><mpath href="#${id}"/></animateMotion></circle>`;}return F(`<svg class="flow-layer" viewBox="0 0 906 360" aria-hidden="true">${s}</svg>`,n,'position:absolute;inset:0');}
const text = (t,x,y,n=1,cls='note',style='') => at(`<div class="${cls}" style="${style}">${t}</div>`,x,y,n);
const count = (n,unit='',digits=0) => `<span data-count="${n}" data-digits="${digits}">${n.toFixed(digits)}</span>${unit}`;
function receipt(name,label,value,x,y,n=1){return F(`${icon(name)}<div class="scene-label">${label}</div>${value?`<div class="receipt-value">${value}</div>`:''}`,n,`left:${x}px;top:${y}px`,'receipt');}
function header(s,i){return `<div class="slide-brand"><span>ALPHA 茶水间</span><span class="folio">${String(i+1).padStart(2,'0')} / ${DECK.slides.length}</span></div><h2 class="slide-title">${esc(s.title)}</h2>${s.source?`<div class="slide-source">${esc(s.source)}</div>`:''}`;}
function graphGrid(){return `<div class="chart-grid">${[40,30,20,10].map((n,i)=>`<div class="grid-line" style="top:${i*58.75}px"><span>${n}%</span></div>`).join('')}</div>`;}
function bars(a=24.4,b=34.1,net=false){return graphGrid()+F(`<div class="bar-comparison"><div class="chart-column"><div class="bar-number strong">${count(a,'%',1)}</div><div class="bar growbar" style="--height:${a*5.875}px"></div><div class="bar-label">中国</div></div><div class="chart-column oecd"><div class="bar-number">${count(b,'%',1)}</div><div class="bar growbar" style="--height:${b*5.875}px"></div><div class="bar-label">OECD平均</div></div></div>`,2,'position:absolute;inset:0')+(net?text('38个OECD国家中，23个低于中国',451,338,3,'small-label strong'): '');}
function taxCategory(name,label,n,dim=false){return F(`<div class="category-icon">${icon(name,label)}</div><div class="scene-label">${label}</div>`,n,'',`tax-category ${dim?'outside-category':''}`);}
const categories = [['purse','工资'],['factory','企业利润'],['cart','消费'],['chart','资本收益'],['house','财产']];
function sourceDiagram(s){let out='';if(s.scene==='exit'||s.scene==='ways'||s.scene==='ending')out+=F(`<div class="source-boundary ${s.scene!=='exit'?'strong-boundary':''}"></div>`,1,'position:absolute;inset:0');
let y=s.scene==='ways'||s.scene==='ending'?73:54;
out+=`<div class="sources-row" style="top:${y}px">${categories.map(([name,label],j)=>figure(name,j===0?'居民收入':label,0,0,69,false,j<2?1:2)).join('')}</div>`;
out+=figure('bank',s.scene==='ending'?'':'财政',405,s.scene==='ending'?188:253,82,false,2);
out+=flow([`M91 ${y+118} C20 233 145 265 437 267`,`M267 ${y+118} C236 250 373 255 437 267`,`M453 ${y+118} L453 247`,`M627 ${y+118} C678 251 530 270 469 267`,`M808 ${y+118} C862 252 586 303 469 267`],2);
if(s.scene==='ways'||s.scene==='ending'){out+=F(`<div class="policy-pills"><span>更严格的征管</span><span>更高的社保实缴</span><span>更少的税收优惠</span>${s.phase===2?'<span>更大的直接税占比</span><span>财产税</span>':''}</div>`,3,'position:absolute;inset:0');}
if(s.scene==='ending')out+=F('<div class="ending-banner">严查税、强化社保，更像是<em>序章</em>。</div>',4,'position:absolute;inset:0');return out;}
function scene(s){let out='';switch(s.scene){
 case 'fiscal':
  out+=figure('bank','离岸信托',108,91,89,true,1)+figure('bag','财政资金',547,94,82,true,2);
  out+=F('<div class="ground-rings" style="left:66px;top:198px;bottom:auto;width:196px;height:56px"></div>',1,'position:absolute;inset:0');out+=flow(['M210 205 C330 157 418 159 555 207'],2)+floatIcon('search',235,79,51,2)+coinGroup(218,205,3,3)+text('钱，够吗？',724,224,3,'note rust');break;
 case 'gap':
  out+=figure('bank','离岸信托',94,82,88,true,1)+figure('bag','财政资金',522,85,81,true,1)+flow(['M201 195 C295 151 407 163 530 200'],1)+coinGroup(197,204,3,1);
  out+=text('新增征管收入',709,21,2,'scene-label')+text(count(5000,'亿元'),690,49,2,'stat strong');
  if(s.phase>=2)out+=F(`<div class="gap-meter"><div class="meter-labels"><span>新增资金缺口</span><span class="rust" style="font-size:24px">${s.phase===2?'2.8万亿元':'还差 2.3万亿元'}</span></div><div class="meter-track"><div class="meter-fill grow-horizontal"></div></div></div>`,3,'position:absolute;inset:0');
  if(s.phase===1)out+=text('严查税 + 强化社保征缴',40,305,3,'hint-pill');
  if(s.phase===3)out+=at('<div class="dark-pill" style="width:202px"><div style="font-size:13px">2030年 · 高盛测算</div><div class="gold-text" style="font-size:22px;white-space:nowrap">缺口或至4.1万亿</div></div>',703,148,4);break;
 case 'gross':out+=bars()+figure('bank','',193,98,63,false,1)+figure('bank','',526,81,63,false,1)+coinGroup(263,51,2,3)+coinGroup(595,24,2,3);break;
 case 'return':out+=bars();out+=F('<div class="return-equation"><b>收走的钱</b><span>−</span><b>公共社会保障支出</b><span>＝</span><b>实收税负</b></div>',3,'position:absolute;inset:0');break;
 case 'net':out+=bars(13.9,12.9,true);break;
 case 'income':
  out+=F(`<div class="income-panel"><div class="scene-label">人均收入</div>${figure('purse','',105,66,78,false,1)}<div class="income-meter"><i class="grow-horizontal"></i></div><div class="note rust" style="position:absolute;left:18px;right:18px;top:217px">约为OECD的四成多</div><div class="welfare-label">${icon('paper')}公共福利仍有距离</div></div>`,1,'position:absolute;inset:0');
  out+=F('<div class="income-bars"><div class="scene-label">实收口径税负</div><div class="bar-comparison"><div class="chart-column"><div class="bar-number strong">13.9%</div><div class="bar growbar" style="--height:81px"></div><div class="bar-label">中国</div></div><div class="chart-column oecd"><div class="bar-number">12.9%</div><div class="bar growbar" style="--height:76px"></div><div class="bar-label">OECD平均</div></div></div></div>',2,'position:absolute;inset:0');break;
 case 'infra':case 'returns':
  out+=figure('road','公路',68,91,72,true,1)+figure('ship','港口',268,62,77,true,1)+figure('plug','电网',461,101,69,true,2)+figure('city','城市',648,67,83,true,2);
  out+=flow(['M29 313 C248 224 349 230 451 273 S713 307 839 251'],2)+floatIcon('coin',6,298,31,2);
  if(s.scene==='infra')out+=coinGroup(790,123,9,3);
  else out+=floatIcon('gear',771,105,47,3)+text('边际回报下降',741,167,3,'note rust')+text('投资回报下降 · 支出转向消费和居民部门',126,332,4,'small-label');break;
 case 'rebalance':
  out+=F(`<div class="rebalance-proposal"><div class="rebalance-card">${icon('purse','居民收入')}<div class="scene-label">更多收入留下来</div><p>居民消费 / 私人投资</p></div><span style="font-size:46px;color:#9aa78f">→</span><div class="rebalance-card">${icon('cart','居民消费')}<div class="scene-label">经济再平衡</div><p>消费与投资</p></div></div>`,1,'position:absolute;inset:0');out+=text('现在想少拿，已经没有过去那么容易。',217,309,2,'note rust');break;
 case 'locked':
  out+=receipt('paper','债务利息','',82,81,1)+receipt('elder','养老金','',357,81,2)+receipt('paper','老龄化支出','',632,81,2);
  out+=F(`<div class="lockline">${icon('lock')}</div>`,3,'position:absolute;inset:0')+text('偿还过去，维持现在',326,293,3,'note rust');break;
 case 'land':
  out+=figure('house','土地与房地产',96,66,83,true,1)+figure('city','银行放贷',350,3,56,false,2)+figure('bank','地方财政',555,98,88,false,2);
  out+=flow(['M216 154 C285 178 285 130 378 131 S482 140 554 139'],2);
  if(s.phase===2){out+=figure('purse','家庭储蓄与现金流',116,253,51,false,3)+flow(['M178 291 C326 342 316 237 321 230 S441 231 597 242'],3)+coinGroup(650,196,3,3)+floatIcon('coin',601,232,31,3)+text('没有直接扣税<br>负担进入房价与土地',430,31,4,'small-label');}break;
 case 'expense':
  out+=text('土地出让收入',33,230,1,'scene-label')+F('<div style="position:absolute;left:33px;top:260px;width:335px;height:19px;background:#d3dbc8"><div class="grow-horizontal" style="height:100%;width:30%;background:var(--teal)"></div></div>',1,'position:absolute;inset:0')+text('较2021年高点下降约70%',33,287,1,'note rust');
  if(s.phase>=2)out+=text('2025年',425,0,2,'small-label')+receipt('paper','广义政府债务','199万亿元',391,36,2)+receipt('bank','2026年利息','约6.2万亿元',640,36,2);
  if(s.phase>=3)out+=floatIcon('elder',462,244,48,3)+text('财政对社保基金补贴',535,218,3,'scene-label')+text('2005年  约600亿元',535,254,3,'note')+text('2026年  超3万亿元',535,287,4,'note rust');
  if(s.phase===1)out+=figure('house','收入退潮',545,44,86,true,2)+text('账单没有一起退',491,238,3,'note rust');break;
 case 'collect':
  out+=receipt('paper','以前没交','',80,64,1)+receipt('bag','以前少交','',361,64,2)+receipt('elder','社保缴费基数','',641,64,2)+figure('bank','',419,279,55,false,3)+flow(['M170 225 C87 309 341 303 451 305','M451 224 L451 290','M731 224 C809 310 582 301 454 304'],3);break;
 case 'rules':
  out+=F(`<div class="collection-grid ${s.phase===2?'collected':'partial'}">${Array.from({length:24},(_,j)=>`<div class="grid-cell">${s.phase===2&&j%3===0?icon('coin'):''}</div>`).join('')}</div>`,1,'position:absolute;inset:0');
  out+=figure('bank','',713,112,91,false,2)+text(s.phase===1?'灵活 → 灰色空间 → 漏洞':'应收尽收',s.phase===1?621:713,228,3,'note rust')+text('名义税率可以不动',155,318,2,'note');
  if(s.phase===2)out+=text('实际负担上升',676,318,3,'note rust');break;
 case 'limits':
  out+=F('<div class="horizontal-chart"><div class="h-row"><div>扩大征管新增资金</div><div class="bar-wrap" style="--width:24.39%"><div class="h-bar grow-horizontal" style="--width:24.39%"></div><div class="h-value">约1万亿 / 年</div></div></div><div class="h-row"><div>土地、债务、社保缺口</div><div class="bar-wrap"><div class="h-bar grow-horizontal" style="--width:100%;background:var(--rust)"></div><div class="h-value">可能达到4.1万亿</div></div></div></div>',2,'position:absolute;inset:0');out+=text('堵住漏洞，也不能凭空创造新的收入来源',194,314,3,'note');break;
 case 'burden':
  out+=F('<div class="burden-card"><div class="scene-label">中国 · 实收口径税负</div><div class="stat">13.9%</div></div>',1,'position:absolute;inset:0')+figure('bank','',657,79,99,false,2)+flow(['M366 185 L606 185'],2)+F('<div style="position:absolute;left:612px;top:260px;width:250px;height:18px;background:#e4c3b2"><div class="grow-horizontal" style="background:var(--teal);height:100%;width:36%"></div></div>',3,'position:absolute;inset:0')+text('财政资金仍不足',612,290,3,'note rust');break;
 case 'taxbase':case 'static':
  out+='<div class="tax-grid"></div>';out+=F(`<div class="tax-boundary ${s.scene==='taxbase'&&s.phase===1?'narrow':''}"></div>`,1,'position:absolute;inset:0');out+=F('<div class="tax-rate">名义税率表 —— 可以不变</div>',1,'position:absolute;inset:0');
  out+=`<div class="tax-categories">${categories.map(([name,label],j)=>taxCategory(name,label,j===0?1:2,s.scene==='taxbase'&&s.phase===1&&j>0)).join('')}</div>`;
  out+=F('<div class="tax-caption">可被财政触及的范围</div>',2,'position:absolute;inset:0');
  if(s.scene==='taxbase'&&s.phase===3)out+=F('<div class="tax-research">未来研究：房产税、遗产税</div>',3,'position:absolute;inset:0');
  if(s.scene==='taxbase'&&s.phase===2)out+=F('<div class="tax-research">扩大纳税人群 · 减少优惠 · 提高实际缴费基数</div>',3,'position:absolute;inset:0');
  if(s.scene==='static'){for(let j=0;j<5;j++)out+=coinGroup(99+j*171,76+(j%2)*13,s.phase===2?3:1,3);out+=F('<div class="tax-research">税率表没动，能征到的钱逐渐变多。</div>',4,'position:absolute;inset:0');}break;
 case 'oldsource':
  out+=F(`<div class="old-finance"><div class="words"><span>土地与房地产</span><span>地方融资平台</span><span>债务扩张</span></div><span style="font-size:43px;color:#8da48a">→</span>${figure('bank','财政',0,0,97,true,2,'')}</div>`,1,'position:absolute;inset:0');break;
 case 'sources':case 'exit':case 'ways':case 'ending':out+=sourceDiagram(s);break;
 default:out+=text(esc(s.phaseName),70,120,1,'stat');
 }return out;}
function canvasHTML(s,i){return `${header(s,i)}<div class="scene-body" data-scene="${s.scene}">${scene(s)}</div><div class="slide-tail"><span>${esc(s.phaseName)}</span><span class="phase-line" style="--progress:${(i+1)/DECK.slides.length*100}%"><i></i></span><span>${s.timeLabel}</span></div>`;}
