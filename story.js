/* 攻略流程版 v0.3：事件与前置条件参考用户指定攻略，连接对白为补写。 */
(()=>{
const S='校园篇 · 学校日常',C='研学篇 · 营地准备',N='夜间篇 · 房间经营';
const initial=()=>({homework:0,notes:0,helpBai:0,paper:0,paperDirect:0,ball:0,rescue:0,team:0,humble:0,win:0,walk:0,food:8,water:8,coins:16,reserve:4,map:0,phone:0,campTurn:0,turn:0,tang:1,tank:1,bai:0,laoda:0,teaGiven:0,cat:0,collar:0,tea:0,check:0,threat:0,visits:0,caught:0});
const room=v=>v.tang+v.tank+v.bai+v.laoda;
const clock=v=>{const t=(21*60+v.turn*15)%(24*60);return `${String(Math.floor(t/60)).padStart(2,'0')}:${String(t%60).padStart(2,'0')}`};
const tick=(v,extra={})=>{v.turn++;for(const[k,n]of Object.entries(extra))v[k]+=n;if(v.turn%4===0){v.food=Math.max(0,v.food-1);v.water=Math.max(0,v.water-1)}};
const choice=(text,next,effect,when)=>({text,next,effect,when});
const nodes=[
{id:'s01',chapter:S,bg:'library',speaker:'旁白',text:'早读前，唐王拿着作业走到桌旁。今天从一件很普通的小事开始。',next:'s-homework'},
{id:'s-homework',chapter:S,bg:'library',speaker:'唐王',text:'作业还差一点。你愿意借我看一下吗？',choices:[choice('借给唐王','s-notes',{homework:1}),choice('拒绝，自己先准备早读','s-notes')]},
{id:'s-notes',chapter:S,bg:'library',speaker:'我',text:'离上课还有几分钟。桌上的笔记翻到了昨天的知识点。',choices:[choice('看一遍笔记','s-question',{notes:1}),choice('先休息一下','s-question')]},
{id:'s-question',chapter:S,bg:'library',speaker:'旁白',text:'上课后，白子被叫起来回答问题。他回头看了我一眼。',choices:[choice('用刚复习的内容提醒白子','s-paper',{helpBai:1},v=>v.notes===1),choice('尝试提醒，但没有复习过答案','s-wrong',null,v=>v.notes===0),choice('不提示，继续听课','s-paper')]},
{id:'s-wrong',chapter:S,bg:'library',speaker:'旁白',text:'提示没有帮上忙。我这才发现，想帮助别人和知道正确答案，是两回事。',next:'s-paper'},
{id:'s-paper',chapter:S,bg:'campus',speaker:'唐王',text:'课间，他从走廊那头求助：能帮忙找点纸吗？',choices:[choice('答应，直接向同学询问','s-ball',{paper:1,paperDirect:1}),choice('答应，悄悄取纸送去','s-ball',{paper:1}),choice('拒绝，先去操场','s-ball')]},
{id:'s-ball',chapter:S,bg:'field',speaker:'旁白',text:'体育课前，一颗乒乓球滚到脚边。远处，钩哥正在找人打球。',choices:[choice('把乒乓球捡起来','s-rescue',{ball:1}),choice('让球留在原地','s-rescue')]},
{id:'s-rescue',chapter:S,bg:'field',speaker:'旁白',text:'白子被拉去陪练，正想回去拿自己的东西。你准备怎样帮他脱身？',choices:[choice('直接上前劝开','s-sport'),choice('递上羽毛球，转移话题','s-sport'),choice('把刚捡到的乒乓球交过去','s-sport',{rescue:1},v=>v.ball===1),choice('先在一旁看球','s-sport')]},
{id:'s-sport',chapter:S,bg:'field',speaker:'钩哥',text:'既然来了，打一局？这次把决定权交给你。',choices:[choice('认真打，选择稳住节奏争取获胜','s-computer',{win:1}),choice('随便打几球，早点结束','s-computer')]},
{id:'s-computer',chapter:S,bg:'library',speaker:'旁白',text:'信息课上，唐王邀请你一起玩枪战游戏。坦克也在旁边招呼你。',choices:[choice('和唐王组队，受压制时保持冷静','s-humble',{team:1}),choice('自己一个人玩','s-cards')]},
{id:'s-humble',chapter:S,bg:'library',speaker:'唐王',text:'配合得不错。你怎么评价刚才这一局？',choices:[choice('谦虚回应，夸夸队友','s-walk',{humble:1}),choice('得意一下，开个玩笑','s-walk')]},
{id:'s-cards',chapter:S,bg:'library',speaker:'坦克',text:'那就和我玩一会儿牌吧。放学后还有时间。',next:'s-walk'},
{id:'s-walk',chapter:S,bg:'campus',speaker:'钩哥',text:'放学了。要不要一起走一段？',choices:[choice('一起走，聊聊今天的事','s-summary',{walk:1}),choice('独自回去','s-summary')]},
{id:'s-summary',chapter:S,bg:'campus',speaker:'学校篇结算',text:v=>{const badges=[];if(v.homework&&v.paperDirect&&v.team&&v.humble)badges.push('真兄弟');if(v.helpBai&&v.rescue)badges.push('英雄救美');if(v.win&&v.walk)badges.push('刚交的朋友');if(!v.homework&&!v.helpBai&&!v.paper&&!v.team)badges.push('独自度过的一天');return `今天的选择已经记录：${badges.join('、')||'平常的一天'}。接下来进入研学篇。`},choices:[choice('进入研学营地','camp-start')]},
{id:'camp-start',chapter:C,bg:'campus',speaker:'旁白',text:'研学集合后，你有四次准备机会。地图和手机能帮助夜间找物资；也可以先准备食物和水。照片沿用校园环境，营地与酒店场景暂用它们代替。',next:'camp-hub'},
{id:'camp-hub',chapter:C,bg:'campus',speaker:'营地探索',text:v=>`准备 ${v.campTurn}/4 · 食物 ${v.food} · 水 ${v.water}。找到需要的东西后，记得及时返回集合点。`,choices:[choice('去公告处找地图','camp-result',{map:1,campTurn:1},v=>!v.map),choice('到失物招领处找到手机','camp-result',{phone:1,campTurn:1},v=>!v.phone),choice('准备食物和饮水','camp-result',{food:4,water:4,campTurn:1}),choice('按时返回大巴，进入夜间篇','n-intro')]},
{id:'camp-result',chapter:C,bg:'cafe',speaker:'旁白',text:'准备完成，集合时间又近了一点。现在检查背包，或者继续做最后的准备。',next:'camp-gate'},
{id:'camp-gate',redirect:v=>v.campTurn>=4?'n-intro':'camp-hub'},
{id:'n-intro',chapter:N,bg:'dorm',speaker:'旁白',text:'晚上九点，唐王与坦克来到你的房间。管理食物和水，接待来访者，留意查房和特殊敲门。每次行动推进十五分钟；探索与事件安排在这版中固定，便于测试。',next:'n-hub'},
{id:'n-hub',chapter:N,bg:'dorm',speaker:'房间管理',text:v=>`${clock(v)} · 房间 ${room(v)} 人（不含自己）。唐王${v.tang?'在':'不在'}，坦克${v.tank?'在':'不在'}，白子${v.bai?'在':'不在'}。${v.map&&v.phone?'地图和手机都在，可以定向寻找关键物品。':'地图或手机未齐，可以去商人处补齐。'} 食物或水为零时，同伴会离开，特殊来访时会更危险。`,choices:[choice('查看手机与地图，外出寻找物资','n-search'),choice('开门接待同学','n-recruit'),choice('与商人交换物品','n-shop'),choice('从备用箱分配食物与水','n-feed',v=>tick(v,{food:2,water:2,reserve:-1}),v=>v.reserve>=1),choice('整理房间，等待下一回合','n-wait',v=>tick(v)),choice('保持房间有人，直接快进到天亮','n-dawn',v=>{v.turn=36;v.food-=2;v.water-=2},v=>room(v)>=2&&v.food>=3&&v.water>=3)]},
{id:'n-search',chapter:N,bg:'campus',speaker:'外出寻找',text:v=>v.map&&v.phone?'手机提供消息，地图标出地点。每次寻找消耗一个回合。':'缺少地图或手机，暂时只能补充普通物资。',choices:[choice('去小卖部找大瓶冰红茶','n-found',v=>tick(v,{tea:1}),v=>v.map&&v.phone),choice('找到猫耳道具','n-found',v=>tick(v,{cat:1}),v=>v.map&&v.phone&&!v.cat),choice('找到铃铛项圈道具','n-found',v=>tick(v,{collar:1}),v=>v.map&&v.phone&&!v.collar),choice('补充食物和水','n-found',v=>tick(v,{food:3,water:3})),choice('返回房间，不消耗回合','n-hub')]},
{id:'n-found',chapter:N,bg:'dorm',speaker:'旁白',text:'物品已经放进背包。回到房间时，走廊安静得让人忍不住留意门口。',next:'n-gate'},
{id:'n-recruit',chapter:N,bg:'dorm',speaker:'同学来访',text:'房间里的人能帮你一起应对夜间事件。选择邀请谁进来；已有的同伴不会重复加入。',choices:[choice('请白子进来','n-joined',v=>tick(v,{bai:1,visits:1}),v=>!v.bai),choice('请牢大进来','n-joined',v=>tick(v,{laoda:1,visits:1}),v=>!v.laoda),choice('请唐王回来','n-joined',v=>tick(v,{tang:1,visits:1}),v=>!v.tang),choice('请坦克回来','n-joined',v=>tick(v,{tank:1,visits:1}),v=>!v.tank),choice('暂不开门，返回房间','n-hub')]},
{id:'n-joined',chapter:N,bg:'dorm',speaker:'旁白',text:'同伴加入了房间。物资、人数和背包里的东西，都会影响下一次敲门。',next:'n-gate'},
{id:'n-shop',chapter:N,bg:'cafe',speaker:'商人',text:v=>`你有 ${v.coins} 元。交易消耗一个回合。地图与手机各 4 元，关键道具各 3 元。`,choices:[choice('买地图（4 元）','n-traded',v=>tick(v,{coins:-4,map:1}),v=>!v.map&&v.coins>=4),choice('买手机（4 元）','n-traded',v=>tick(v,{coins:-4,phone:1}),v=>!v.phone&&v.coins>=4),choice('买猫耳道具（3 元）','n-traded',v=>tick(v,{coins:-3,cat:1}),v=>!v.cat&&v.coins>=3),choice('买铃铛项圈道具（3 元）','n-traded',v=>tick(v,{coins:-3,collar:1}),v=>!v.collar&&v.coins>=3),choice('买大瓶冰红茶（3 元）','n-traded',v=>tick(v,{coins:-3,tea:1}),v=>v.coins>=3),choice('返回房间','n-hub')]},
{id:'n-traded',chapter:N,bg:'dorm',speaker:'旁白',text:'交易完成，物品和余额已经更新。',next:'n-gate'},
{id:'n-feed',chapter:N,bg:'dorm',speaker:'旁白',text:'大家从备用箱中取出食物和水，库存减少了一份。这版把进食饮水简化为小组共享补给。',choices:[choice('继续管理房间','n-gate'),choice('给牢大一瓶冰红茶','n-tea',v=>{v.tea--;v.teaGiven++},v=>v.laoda&&v.tea>=1)]},
{id:'n-tea',chapter:N,bg:'dorm',speaker:'牢大',text:v=>`谢谢。已经给了 ${v.teaGiven} 瓶；第三瓶之后，他会在特殊来访中帮忙。`,next:'n-gate'},
{id:'n-wait',chapter:N,bg:'dorm',speaker:'旁白',text:'十五分钟过去了。你再次清点房间里的人和剩下的补给。',next:'n-gate'},
{id:'n-gate',redirect:v=>{if(!v.food||!v.water){v.tang=0;v.tank=0;v.bai=0;v.laoda=0}if(v.turn>=36)return 'end-false';if(v.turn>=2&&Math.floor(v.turn/4)+1>v.check)return 'n-inspect';if(v.turn>=4&&Math.floor(v.turn/4)>v.threat)return 'n-knock';return 'n-hub'}},
{id:'n-inspect',chapter:N,bg:'dorm',speaker:'教官查房',text:'走廊传来查房声。桌底、衣柜、卫生间和阳台都能安排同伴躲藏。确认安排后，时间继续推进。',choices:[choice('安排所有人在不同位置躲好','n-hidden',v=>{v.check=Math.floor(v.turn/4)+1}),choice('留在原地不躲藏','n-cleared',v=>{v.caught+=room(v);v.tang=0;v.tank=0;v.bai=0;v.laoda=0;v.check=Math.floor(v.turn/4)+1})]},
{id:'n-hidden',chapter:N,bg:'dorm',speaker:'旁白',text:'查房结束，大家重新回到房间。这里把藏身操作简化为一次统一安排。',next:'n-gate'},
{id:'n-cleared',chapter:N,bg:'dorm',speaker:'旁白',text:'没有藏好的同伴被带离了房间。下一次特殊敲门前，需要考虑重新邀请同学。',next:'n-gate'},
{id:'n-knock',chapter:N,bg:'dorm',speaker:'白钩',text:'敲门声再一次响起。门外的来访者问起房间里的人。先查看同伴和物品，再决定怎样应对。',choices:[choice('让唐王、坦克和白子一起回应，并拿出三件关键物品','end-true',v=>{v.threat=Math.floor(v.turn/4)},v=>v.tang&&v.tank&&v.bai&&v.cat&&v.collar&&v.tea>=1),choice('请已喝过三瓶冰红茶的牢大出面','end-laoda',null,v=>v.laoda&&v.teaGiven>=3),choice('说明房里有人，先守住这一轮','n-safe',v=>{v.threat=Math.floor(v.turn/4)},v=>room(v)>=2),choice('独自应对门外的人','end-caught',null,v=>room(v)<2)]},
{id:'n-safe',chapter:N,bg:'dorm',speaker:'旁白',text:'这一轮暂时平安。仅仅等到天亮还不一定是真正的结束；可以继续准备同伴与关键物品。',next:'n-hub'},
{id:'n-dawn',chapter:N,bg:'dorm',speaker:'旁白',text:'你决定守住现状，快进度过剩下的夜晚。补给减少了一些，窗外终于亮了。',next:'end-false'},
{id:'end-false',chapter:'结局 · 天亮',bg:'gate',speaker:'旁白',text:'你和同伴等到了天亮，但这只是表面的结束。还有另一条路线藏在同伴与物品条件里。',ending:'我们安全了？',epilogue:'假结局 · 仅仅熬到天亮。\n提示：准备指定同伴和三件物品，再面对特殊敲门。'},
{id:'end-true',chapter:'结局 · 条件齐备',bg:'campus',speaker:'旁白',text:'三位同伴都在，三件关键物品也已经准备好。你们一起面对来访者，终于走到了另一种结局。',ending:'简单又复杂',epilogue:'真结局条件达成。\n唐王、坦克、白子在场；猫耳、铃铛项圈、大瓶冰红茶齐备。\n结尾对白为本试玩版补写。'},
{id:'end-laoda',chapter:'结局 · 牢大出面',bg:'field',speaker:'旁白',text:'来访者正要闯进来，牢大站到了门前。这一次，夜间的危机被他挡了下来。',ending:'牢大出面',epilogue:'特殊结局 · 牢大在场，并已收到三瓶冰红茶。\n这版用文字结算表现事件。'},
{id:'end-caught',chapter:'结局 · 房间无人',bg:'dorm',speaker:'旁白',text:'房间里没有足够的人帮忙。特殊来访打断了这一夜，游戏在这里结束。',ending:'第一次失守',epilogue:'失败结局。\n可以读取前面的存档，补充食物和水，重新邀请同伴。'}
];
function view(n,v){if(!n)return null;return {...n,text:typeof n.text==='function'?n.text(v):n.text}}
window.STORY={start:'s01',nodes,initial,view,validate(v){const d=initial();return !!v&&Object.keys(d).every(k=>Number.isInteger(v[k])&&v[k]>=0&&v[k]<=100)&&['tang','tank','bai','laoda','map','phone','cat','collar'].every(k=>v[k]<=1)&&v.campTurn<=4&&v.turn<=36},status(v,n){if(n?.chapter?.startsWith('校园'))return `笔记 ${v.notes?'已看':'未看'} · 帮助白子 ${v.helpBai?'已完成':'未完成'} · 乒乓球 ${v.ball?'已捡':'未捡'}`;return `食物 ${v.food} · 水 ${v.water} · ¥${v.coins} · 同伴 ${room(v)} · ${clock(v)}\n地图 ${v.map?'✓':'—'} / 手机 ${v.phone?'✓':'—'} / 猫耳 ${v.cat?'✓':'—'} / 项圈 ${v.collar?'✓':'—'}\n冰红茶 ${v.tea} 瓶 · 已给牢大 ${v.teaGiven}/3 · 备用补给 ${v.reserve}`}};
})();
