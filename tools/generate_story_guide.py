from pathlib import Path
import json, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, XPreformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('ZH','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=0))
WINE=colors.HexColor('#794858'); INK=colors.HexColor('#342d39'); MUTED=colors.HexColor('#796b75'); PALE=colors.HexColor('#f7f1ee'); GOLD=colors.HexColor('#d7b88c')
styles={
 'title':ParagraphStyle('title',fontName='ZH',fontSize=31,leading=43,textColor=WINE,spaceAfter=19,wordWrap='CJK'),
 'h1':ParagraphStyle('h1',fontName='ZH',fontSize=21,leading=30,textColor=WINE,spaceAfter=17,wordWrap='CJK'),
 'h2':ParagraphStyle('h2',fontName='ZH',fontSize=12.5,leading=20,textColor=WINE,spaceBefore=12,spaceAfter=7,wordWrap='CJK'),
 'body':ParagraphStyle('body',fontName='ZH',fontSize=10.2,leading=18,textColor=INK,spaceAfter=8,wordWrap='CJK'),
 'small':ParagraphStyle('small',fontName='ZH',fontSize=8.3,leading=14,textColor=MUTED,spaceAfter=7,wordWrap='CJK'),
 'code':ParagraphStyle('code',fontName='ZH',fontSize=8.5,leading=13,textColor=INK,leftIndent=10,rightIndent=10,spaceBefore=8,spaceAfter=10),
 'cell':ParagraphStyle('cell',fontName='ZH',fontSize=9,leading=15,textColor=INK,wordWrap='CJK'),
}
repo='https://github.com/seanxhr137/after-class-demo'
site='https://seanxhr137.github.io/after-class-demo/'
pages=[
('从这里开始',[
('title','肉と便の恋\n剧情编辑教程'),
('p','给获得授权的剧情协作者。无需安装编辑器，先学会在 GitHub 网页上修改一句台词，再尝试增加对白与调整选项。'),
('box','唯一剧情源：story.json\n直接提交到 main → 自动检查 → 自动构建 → 更新同一个游戏网址'),
('h','先打开这三个入口'),
('link',('游戏仓库',repo)),('link',('在线游戏',site)),('link',('直接编辑 story.json',repo+'/edit/main/story.json')),
('h','谁可以做什么'),
('table',(['身份','权限'],[['普通访客','可以游玩和查看公开源码，不能直接修改主仓库。'],['受邀协作者','接受邀请后，可直接编辑、提交到 main，并触发发布。'],['所有者 seanxhr137','邀请或移除协作者，处理误改与权限。']])),
('p','当前尚未添加其他协作者，名单由所有者稍后提供。人物素材也由所有者后续提供；现阶段保留姓名占位牌。'),
('small','适用版本：视觉小说版 v0.4。2026-11-12。旧资源管理版的教程与存档不适用于本版。')]),
('所有者与协作者的准备',[
('h1','01 先获得修改权限'),
('h','所有者：只邀请你允许的人'),
('steps',['打开游戏仓库，进入 Settings。','进入 Collaborators（有时位于 Access 分组），点击 Add people。','输入对方准确的 GitHub 用户名，核对账号后发送邀请。','让对方接受邀请；在协作者列表中确认邀请已接受。']),
('box','协作者写权限覆盖整个仓库，不会只限于 story.json。\n不要为普通剧情编辑者授予管理员权限；仅邀请你信任的人。'),
('h','协作者：接受后再开始'),
('steps',['登录被邀请的同一个 GitHub 账号，在通知或邀请邮件中接受邀请。','打开仓库里的 story.json，点击铅笔图标 Edit this file。','保存时，如果能选择直接提交到 main，说明当前账号具有相应写权限。']),
('p','如果只看到“Fork this repository”或“Propose changes”，说明当前还不能直接改主仓库。先检查账号是否正确、邀请是否接受，再联系所有者。不要把 Fork 中的修改当成已经更新了主游戏。'),
('link',('所有者的协作者设置',repo+'/settings/access')),
('h','不再允许某人修改时'),
('p','所有者在同一协作者设置中移除该账号即可。公开源码仍可查看，但该账号不再具有直接写入主仓库的权限。'),
('small','GitHub 按钮名称可能随语言与界面变化。核心是：所有者邀请 → 对方接受 → 对方直接提交主仓库。')]),
('第一次：只改一句台词',[
('h1','02 五分钟完成第一次修改'),
('steps',['打开 story.json，点击铅笔进入编辑。','用浏览器查找 opening-01，定位第一句的 text 字段。','只改双引号里面的中文，保留字段名、引号和行尾逗号。','点击 Commit changes，填写说明，例如“修改序章第一句旁白”。','选择直接提交到 main，再点击确认提交。']),
('h','修改前'),
('code','"text": "雨停在最后一节课结束前。校门外的路面还湿着，风里有一点树叶和泥土的味道。",'),
('h','修改后：示范写法，不要求照抄'),
('code','"text": "放学铃响了。校门外的路面还湿着，晚风正从树梢间吹过。",'),
('box','最稳妥的第一次修改：只改 text，其他内容保持原样。\n改完无需手动运行 build.py，也不用再改任何 vn-story 文件。'),
('h','提交之后去哪里看'),
('p','进入仓库 Actions，打开与你本次提交对应的 “Check story and publish game”。检查和发布都变成绿色后，再打开游戏，从新游戏进入刚修改的场景。'),
('p','不要用一个较后的存档来验证第一句。存档会恢复到保存的位置，并不自动回到开场。'),
('link',('查看自动检查与发布',repo+'/actions'))]),
('认识剧情数据',[
('h1','03 只认识需要改的字段'),
('table',(['字段','含义与写法'],[['text','当前句台词、旁白或内心独白。'],['speaker','说话人编号：me、tang、bai；thought 表示主角内心，narration 表示旁白。'],['id','当前句的唯一编号。已有编号尽量保留，不能重复。'],['next','下一句的 id。不是行数，也不是章节标题。'],['chapter','画面左上角的场景名称。'],['bg','背景文件名，不含 assets/ 和 .jpg，例如 cafe。'],['cast','场上角色、左右站位与表情。me 是主角，通常在左侧。'],['choices / ending','关键选项或结尾；与 next 三者只能选一种。']])),
('h','角色编号与显示姓名'),
('p','在 actors 中，me 是主角、tang 是唐王、bai 是白子。修改 name 可以改变画面上的姓名；不要只把 speaker 改成中文姓名，因为 speaker 需要使用已定义的角色编号。'),
('h','现有背景'),
('p','campus：校门集合；library：图书馆；cafe：书吧；field：操场；dorm：宿舍；gate：校门。文件位于 assets，均为历史照片。'),
('h','JSON 的三个常见规则'),
('steps',['字段名和字符串两端使用英文半角双引号。中文内容里可以使用“中文引号”。','同一对象的字段之间用英文逗号；最后一项后不要多加逗号。','字符串中想换行时写 \\n，不要在双引号尚未结束时直接按回车换行。']),
('small','id、version、start 和故事顶层结构不要随意改。大幅调整旧台词编号或删除场景前，先与所有者商量存档兼容问题。')]),
('增加一句对白',[
('h1','04 把新句子插入剧情链'),
('p','示例：在 opening-01 后面插入一句主角内心。原来的连接是 opening-01 → opening-02。现在要变成 opening-01 → opening-01a → opening-02。'),
('steps',['先把 opening-01 的 next 改为 opening-01a。','在 nodes 数组中，复制下面的新对象，放在 opening-01 后面。','确认对象之间用逗号分隔，编号不重复，再提交检查。']),
('code','''{
  "id": "opening-01a",
  "speaker": "thought",
  "text": "原来，我比自己想象中更期待再见到他们。",
  "bg": "campus",
  "chapter": "序章 · 又一次，放学以后",
  "cast": [
    {"actor": "me", "position": "left", "expression": "犹豫"},
    {"actor": "tang", "position": "right", "expression": "等待"}
  ],
  "next": "opening-02"
}'''),
('box','先接入，再提交：只增加一个对象却不修改上一句的 next，\n新句子就不会被读到，检查也会提示“无法从开始到达”。'),
('h','删除一句时'),
('p','先把指向它的 next 或选项 next 接到下一句，再删除它。不要让任何跳转还指向被删掉的 id；不确定时先只改台词，等所有者确认后再删除。'),
('small','建议每句保持一两句话。太长的旁白分成几句，手机上更容易阅读，也更像视觉小说的节奏。')]),
('选项、结局与人物素材',[
('h1','05 修改分支，不改运行代码'),
('p','找到 choice-01。只改选项文案时，修改 choices 里的 text，保留 next 与 route 即可。每个选择点支持 2-4 个选项。'),
('code','''"choices": [
  {
    "text": "「走吧。我想坐在离你最近的地方。」",
    "next": "close-01",
    "route": "near"
  },
  {
    "text": "「先陪我走一圈吧，我有话想说。」",
    "next": "walk-01",
    "route": "walk"
  }
]'''),
('p','next 必须指向已存在的台词 id。新增分支时，先写好目标场景，再连接选项；route 使用清楚的英文编号，例如 friendship，不需要修改 app.js。'),
('h','结尾字段'),
('p','结尾的 ending 包含 id、title 和 text。title 是结尾标题，text 是结尾说明。结尾节点不要再放 next 或 choices。'),
('h','人物素材由所有者之后提供'),
('p','当前 actors 中的 image 保留 null。expression 先写“微笑”“认真”等文字，作为表情占位；正式素材到齐后，由所有者设置 image 或 expressions 映射。不要擅自从视频截图截取人物加入游戏。'),
('small','配音 voice、音乐 bgm、演员图片等路径只有在文件已经放进 assets 后才填写。缺失文件会阻止发布。当前无需准备这些素材。')]),
('检查、恢复与交付',[
('h1','06 出错时这样处理'),
('table',(['看到的情况','处理方式'],[['Actions 红色：JSON 错误','回到刚改的地方，检查双引号、逗号和花括号。'],['提示 id 重复','给新增句子换一个唯一 id，再核对指向它的 next。'],['提示跳转目标不存在','复制目标句的 id，替换拼错的 next；不要填行号。'],['提示无法到达或无法结局','补好剧情连接，确保从 start 能读到新增句，并能走向结尾。'],['Actions 绿色，但没看到新句','确认看的提交是自己的最新提交；从新游戏进入，必要时刷新。'],['旧存档读不了','大改编号或故事标识可能影响存档。先通知所有者，不要清除别人的数据。']])),
('h','误改了整段，如何恢复'),
('steps',['在 story.json 页面点击 History，找到修改前的版本。','打开该版本的文件，查看 Raw，复制需要恢复的内容。','回到 main 当前的 story.json，点击铅笔，贴回正确内容。','提交说明写“恢复某段剧情”，等检查与发布再次成功。']),
('p','检查失败时，线上继续保留上一次成功发布的游戏。先修好错误再提交，不需要删除仓库，也不要强制重置主分支。'),
('h','提交前的最后四项'),
('p','① text 与 speaker 正确　② 新 id 不重复、next 已接好\n③ 不修改未提供的人物素材　④ 提交后确认 Actions 绿色'),
('small','官方参考：GitHub Docs - 邀请个人仓库协作者；Using custom workflows with GitHub Pages。访问日 2026-11-12。'),
('link',('GitHub Pages 工作流说明','https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages'))])
]

story=[];md=['# 肉と便の恋：剧情编辑教程','\n版本：v0.4 / 2026-11-12\n']
def p(text,style='body'):
 return Paragraph(html.escape(text).replace('\n','<br/>'),styles[style])
def table(headers,rows):
 cells=[[p(x,'cell') for x in headers]]+[[p(x,'cell') for x in row] for row in rows]
 t=Table(cells,colWidths=[128,363],hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eddfdb')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#c4a5a5'))]))
 return t
for index,(label,items) in enumerate(pages):
 if index:story.append(PageBreak())
 md+=['\n## '+label+'\n']
 for kind,value in items:
  if kind in ['title','h1','h','p','small']:
   style={'title':'title','h1':'h1','h':'h2','p':'body','small':'small'}[kind];story.append(p(value,style));md.append(('### ' if kind=='h' else '')+value+'\n')
  elif kind=='box':
   t=Table([[p(value)]],colWidths=[491]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#dbc9c3')),('LEFTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([Spacer(1,6),t,Spacer(1,8)]);md.append('> '+value.replace('\n','\n> ')+'\n')
  elif kind=='steps':
   for i,text in enumerate(value,1):story.append(p(f'{i}. {text}'));md.append(f'{i}. {text}')
   md.append('')
  elif kind=='code':
   code=XPreformatted(html.escape(value),styles['code']);t=Table([[code]],colWidths=[491]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#e3d4ce')),('LEFTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.extend([t,Spacer(1,8)]);md+=['```json',value,'```\n']
  elif kind=='link':
   label,url=value;story.append(Paragraph(f'<link href="{html.escape(url,quote=True)}" color="#794858"><u>{html.escape(label)}</u></link>',styles['body']));md.append(f'[{label}]({url})\n')
  elif kind=='table':
   headers,rows=value;story.extend([table(headers,rows),Spacer(1,8)]);md.append('| '+' | '.join(headers)+' |');md.append('| --- | --- |');md.extend('| '+' | '.join(row)+' |' for row in rows);md.append('')
(OUT/'剧情编辑教程.md').write_text('\n'.join(md),encoding='utf-8')

def frame(canvas,doc):
 canvas.setTitle('肉と便の恋 - 剧情编辑教程');canvas.setAuthor('肉と便の恋项目')
 w,h=doc.pagesize
 canvas.setStrokeColor(GOLD);canvas.setLineWidth(1);canvas.line(52,h-37,w-52,h-37)
 canvas.setFillColor(MUTED);canvas.setFont('ZH',8);canvas.drawString(52,h-28,'肉と便の恋 / 剧情协作指南')
 canvas.setStrokeColor(colors.HexColor('#e2d5cd'));canvas.line(52,43,w-52,43)
 canvas.setFillColor(MUTED);canvas.drawString(52,29,'只修改 story.json · 检查通过后自动上线')
 canvas.drawRightString(w-52,29,f'{doc.page} / 7')
doc=SimpleDocTemplate(str(OUT/'剧情编辑教程.pdf'),pagesize=(595.28,841.89),leftMargin=52,rightMargin=52,topMargin=59,bottomMargin=59)
doc.build(story,onFirstPage=frame,onLaterPages=frame)
print(OUT/'剧情编辑教程.pdf')
