function pageAuditIds(s){return [...new Set([...s.auditIds,...(comparisonFor(s)?.auditIds??[])])];}
function renderComparison(s){
 const c=comparisonFor(s),available=DECK.slides.filter(comparisonFor),ids=pageAuditIds(s),button=$('checked-view');
 button.disabled=!c;button.setAttribute('aria-pressed',String(CHECKED_VIEW));button.textContent=c?(CHECKED_VIEW?'返回原视频重绘':c.kind==='source'?'查看原文对照':'查看本页差异'):'本页无画面差异';button.title=c?c.summary:'当前页没有另一套校核画面；审计说明可从右侧查看。';
 $('comparison-panel').classList.toggle('comparing',CHECKED_VIEW);$('comparison-panel').dataset.kind=c?.kind??'none';
 $('comparison-status').textContent=c?`${c.label} · ${CHECKED_VIEW?'正在查看校核画面':'当前为原视频重绘'}`:ids.length?'本页有审计说明，画面保留':'本页没有图形或文案差异';
 $('comparison-summary').textContent=c?c.summary:'本页没有另一套校核画面，切换不会增加信息。画面保留不代表所有内容已核验无误；具体依据和资料缺口见审计。';
 $('comparison-details').hidden=!c;$('comparison-original').textContent=c?.original??'';$('comparison-checked').textContent=c?.checked??'';
 $('comparison-directory').textContent=`可对照的页 ${available.length}/${DECK.slides.length}`;$('comparison-next').disabled=available.length===0;$('comparison-directory').disabled=available.length===0;$('comparison-audit').hidden=ids.length===0;
}
function renderAudit(s){
 const ids=pageAuditIds(s),findings=DECK.audit.findings.filter(c=>AUDIT_ALL||ids.includes(c.id));
 const names={issue:'内部不一致',limited:'证据／范围限制',inference:'推演与表述边界',pass:'核验一致（限定范围）'};
 document.getElementById('audit-scroll').innerHTML=`<div class="case-note">${esc(DECK.audit.summary)}。校核对照不会修改原视频讲稿。</div><button class="audit-all" id="all-audits">${AUDIT_ALL?'仅看当前页审计':'查看全片审计报告'} · ${DECK.audit.findings.length}项</button>`+findings.map(c=>`<article class="audit-card"><span class="result ${c.status}">${c.id} · ${names[c.status]}</span><h3>${esc(c.title)}</h3><p><b>原表述：</b>${esc(c.claim)}</p><p>${esc(c.evidence)}</p>${c.calculation?`<div class="math">${esc(c.calculation)}</div>`:''}${c.scope?`<p class="small-label">${esc(c.scope)}</p>`:''}<p><a href="${DECK.source}?t=${c.times[0]}" target="_blank" rel="noopener">原视频 ${c.times[0]}秒 ↗</a>　<button class="audit-jump" data-time="${c.times[0]}">查看对应页</button></p></article>`).join('')+(findings.length?'':'<div class="case-note">当前页没有单独列出的审计项。可查看全片报告或来源清单。</div>');
 document.getElementById('all-audits').onclick=()=>{AUDIT_ALL=!AUDIT_ALL;renderAudit(DECK.slides[state.index]);};
 document.querySelectorAll('.audit-jump').forEach(b=>b.onclick=()=>renderSlide(slideAt(Number(b.dataset.time))));
 document.getElementById('sources-scroll').innerHTML='<div class="case-note">'+esc(DECK.audit.summary)+'</div>'+DECK.audit.sources.map(s=>`<div class="source-entry"><b>${s.id} · ${esc(s.title)}</b><small>${esc(s.date??'')} ${esc(s.issue??'')} · ${esc(s.publisher??'')}</small><small>${esc(s.status)}</small>${(s.excerpts??[]).map(e=>`<p><b>${esc(e.location)}</b><br>“${esc(e.text)}”</p>`).join('')}${s.url?`<a href="${esc(s.url)}" target="_blank" rel="noopener">查看原始出处 ↗</a>`:'<small>非公开资料，无网页发布附件。</small>'}</div>`).join('');
 const cls=DECK.slides[state.index].theme;document.getElementById('canvas').className='canvas '+cls;
}
document.querySelectorAll('.audit-tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.audit-tabs button').forEach(n=>n.classList.toggle('selected',n===b));document.getElementById('subtitle-scroll').hidden=b.dataset.panel!=='transcript';document.getElementById('audit-scroll').hidden=b.dataset.panel!=='audit';document.getElementById('sources-scroll').hidden=b.dataset.panel!=='sources';});
document.getElementById('checked-view').onclick=()=>{const s=DECK.slides[state.index];if(!comparisonFor(s))return;CHECKED_VIEW=!CHECKED_VIEW;stage.innerHTML=canvasHTML(s,state.index);state.step=1;state.maxStep=Math.max(...[...stage.querySelectorAll('[data-order]')].map(n=>Number(n.dataset.order)),1);fragments();renderComparison(s);};
document.getElementById('comparison-directory').onclick=()=>gallery(true);
document.getElementById('comparison-next').onclick=()=>{const indexes=DECK.slides.map((s,i)=>comparisonFor(s)?i:-1).filter(i=>i>=0);if(!indexes.length)return;const next=indexes.find(i=>i>state.index)??indexes[0];CHECKED_VIEW=true;renderSlide(next);};
document.getElementById('comparison-audit').onclick=()=>{AUDIT_ALL=false;renderAudit(DECK.slides[state.index]);document.querySelector('[data-panel="audit"]').click();};
