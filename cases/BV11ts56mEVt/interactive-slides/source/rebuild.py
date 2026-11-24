from pathlib import Path
import json
from html import escape
source=Path(__file__).resolve().parent
dest=source.parent
data=json.loads((dest/'slides-data.json').read_text())
template=(source/'template.html').read_text()
tokens=[('/*__STYLE__*/',(source/'style.css').read_text()+'\n'+(source/'audit.css').read_text()),('<!--__ICONS__-->',(source/'icons.svg').read_text()),('/*__DATA__*/',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')),('/*__RENDER__*/',(source/'render.js').read_text()),('/*__APP__*/',(source/'app.js').read_text()),('/*__AUDIT_APP__*/',(source/'audit-app.js').read_text()),('__AUTHOR__',escape(data['author'])),('__TITLE__',escape(data['title'])),('__CASE__',data['caseId'])]
for token,content in tokens:template=template.replace(token,content)
(dest/'index.html').write_text(template)
print('Built audit deck:',data['caseId'],len(data['slides']),'pages')
