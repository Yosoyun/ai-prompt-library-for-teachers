#!/usr/bin/env python3
"""Build 'Prompt Studio' — Ivory Editorial, Teacher/Student modes, JEE/NEET/Olympiad/Foundation.
Run: python3 build_site.py
"""
import json, html, os, datetime

HERE=os.path.dirname(os.path.abspath(__file__))
raw=json.load(open(os.path.join(HERE,"data","prompts.json"),encoding="utf-8"))

AUTHOR="Indrajeet Yadav"; ROLE="Maths Faculty"; BRAND="Prompt Studio"
TAGLINE="Premium, ready-to-use AI prompts for every teacher and student."
BUILD=datetime.date.today().isoformat()
SITE_URL="https://yosoyun.github.io/ai-prompt-library-for-teachers/"
CONTACT={"email":"indrajeetsirallen@gmail.com","wa_num":"918072965053","insta":"indrajeetsirallen"}
FEEDBACK_FORM_URL=""
TOOLS=[
 {"name":"Maths Prompt Studio","desc":"136+ AI prompts for maths teachers — solutions, papers, worksheets, DPPs.","url":"https://yosoyun.github.io/math-prompt-studio/"},
 {"name":"Ranker Masterbooks","desc":"ARC & LIMITS — 200 original multi-method problems, Python-verified.","url":"https://yosoyun.github.io/ranker-masterbooks/"},
 {"name":"Andreescu Library","desc":"A searchable guide to every book by Titu Andreescu.","url":"https://yosoyun.github.io/andreescu-library/"},
 {"name":"LIMITS Masterbook","desc":"100 ranker-level limit problems (JEE Advanced / Olympiad).","url":"https://limits-masterbook.vercel.app"},
]
MODES=["Teacher","Student"]
TRACK_ORDER=["JEE","NEET","Olympiad","Foundation"]
TRACK_LABEL={"JEE":"JEE","NEET":"NEET","Olympiad":"Olympiad","Foundation":"Foundation & Boards"}
LEVELS=["School (6–10)","Boards (11–12)","JEE / NEET","Olympiad","Any"]

def varlist(v):
    if isinstance(v,list): return [str(x).strip() for x in v if str(x).strip()]
    if not v: return []
    import re; return [x.strip() for x in re.split(r"[,\n]",str(v)) if x.strip()]

prompts=[]
for i,p in enumerate(raw,1):
    mode=p.get("mode","Teacher"); mode=mode if mode in MODES else "Teacher"
    track=p.get("track","Foundation"); track=track if track in TRACK_ORDER else "Foundation"
    lv=p.get("level") or ["Any"]
    if isinstance(lv,str): lv=[lv]
    lv=[x for x in lv if x in LEVELS] or ["Any"]
    prompts.append({"id":p.get("id",f"P{i:04d}"),"mode":mode,"track":track,
      "subject":(p.get("subject") or "General").strip(),"category":(p.get("category") or "General").strip(),
      "title":(p.get("title") or "Untitled").strip(),"use_case":(p.get("use_case") or "").strip(),
      "what_you_get":(p.get("what_you_get") or p.get("use_case") or "").strip(),"level":lv,
      "output_type":"image" if str(p.get("output_type","")).lower()=="image" else "text",
      "interactive":bool(p.get("interactive",False)),"variables":varlist(p.get("variables",[])),
      "prompt":(p.get("prompt") or "").strip(),"tool":(p.get("tool") or "Any").strip()})
COUNT=len(prompts)
def fc(**kw): return sum(1 for p in prompts if all(p.get(k)==v for k,v in kw.items()))

def esc(s): return html.escape(s or "",quote=True)
def jsemb(o): return json.dumps(o,ensure_ascii=False).replace("</","<\\/")

WA={
"Invite (English)":"🎓 *"+BRAND+" — for teachers & students*\n\n"+str(COUNT)+"+ premium, copy-paste AI prompts for JEE, NEET, Olympiad & school — solutions, mock papers, doubt-solving, study plans, lesson plans and more. Many ask you a few questions first, then give a premium answer. Attach a photo of any question and they solve it.\n\n✅ Works on ChatGPT, Claude or Gemini (free too).\n🧩 Pick Teacher or Student → choose a prompt → fill the [BLANKS] → paste.\n\n👉 "+SITE_URL+"\n\nMade for teachers & students, by "+AUTHOR+".",
"How to use it daily (English)":"📌 *How to use "+BRAND+" every day*\n\n1️⃣ Open the link, bookmark it.\n2️⃣ Tap *Teacher* or *Student* mode.\n3️⃣ Pick your track — JEE / NEET / Olympiad / Foundation — and subject.\n4️⃣ Tap *Copy*, paste into ChatGPT / Claude / Gemini.\n5️⃣ Answer its questions (many ask first), or attach your question's photo.\n6️⃣ Get a premium, exam-accurate answer — signed so you can reach me.\n\n👉 "+SITE_URL,
"Invite (Hindi)":"🎓 *"+BRAND+" — शिक्षकों और छात्रों के लिए*\n\n"+str(COUNT)+"+ प्रीमियम, कॉपी-पेस्ट AI प्रॉम्प्ट — JEE, NEET, Olympiad और स्कूल के लिए। हल, मॉक पेपर, डाउट सॉल्विंग, स्टडी प्लान और बहुत कुछ। कई प्रॉम्प्ट पहले आपसे सवाल पूछते हैं, फिर प्रीमियम उत्तर देते हैं। सवाल की फोटो लगाओ — हल हो जाएगा।\n\n✅ ChatGPT, Claude या Gemini पर चलता है।\n👉 "+SITE_URL+"\n\n— "+AUTHOR,
}

CONFIG={"brand":BRAND,"author":AUTHOR,"role":ROLE,"site":SITE_URL,"count":COUNT,
 "contact":CONTACT,"form":FEEDBACK_FORM_URL,"tools":TOOLS,"modes":MODES,
 "trackOrder":TRACK_ORDER,"trackLabel":TRACK_LABEL,"levels":LEVELS,"wa":WA}

TEMPLATE=r"""<!DOCTYPE html>
<html lang="en" data-theme="day">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="description" content="__COUNT__+ premium copy-paste AI prompts for teachers and students — JEE, NEET, Olympiad and school. Interview-first, photo-aware. Works with ChatGPT, Claude, Gemini."/>
<meta name="theme-color" content="#f7f1e6"/>
<title>__BRAND__ · __COUNT__+ premium AI prompts for teachers & students</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,900;1,9..144,400;1,9..144,500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#f7f1e6;--paper:#fffdf7;--paper-2:#fbf6ec;--ink:#211d16;--ink-2:#4a4338;--ink-3:#6f685a;
 --line:#211d1622;--line-2:#211d1610;--em:#1c4a3a;--em-ink:#123528;--em-soft:#1c4a3a14;--sienna:#9a4a2a;--gold:#a9772a;--blue:#2f5d86;
 --f-disp:"Fraunces",Georgia,serif;--f-serif:"Newsreader",Georgia,serif;--f-ui:"Hanken Grotesk",-apple-system,sans-serif;--f-mono:"JetBrains Mono",ui-monospace,monospace;--maxw:1140px;}
html[data-theme="ink"]{--bg:#15120c;--paper:#1e1a12;--paper-2:#241f15;--ink:#ece3d2;--ink-2:#b6ab95;--ink-3:#8a8070;
 --line:#ffffff1f;--line-2:#ffffff10;--em:#7cc6a3;--em-ink:#bfe7d4;--em-soft:#7cc6a31a;--sienna:#df9468;--gold:#e2b667;--blue:#8fb8de;}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--f-ui);font-size:16px;line-height:1.55;
 background-image:radial-gradient(var(--line-2) 1px,transparent 1px);background-size:22px 22px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}::selection{background:var(--em);color:var(--bg)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 40px}
@media(max-width:640px){.wrap{padding:0 20px}}
.sc{font-family:var(--f-ui);font-size:12px;font-weight:600;letter-spacing:2.4px;text-transform:uppercase}
header.nav{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav .row{display:flex;align-items:center;gap:20px;height:66px}
.brand{display:flex;align-items:center;gap:11px;font-family:var(--f-disp);font-weight:600;font-size:20px;letter-spacing:-.3px}
.brand .seal{width:34px;height:34px;border:1.5px solid var(--em);border-radius:50%;display:grid;place-items:center;font-family:var(--f-disp);font-style:italic;color:var(--em);font-size:17px}
.nav nav{display:flex;gap:26px;margin-left:auto;font-size:14px;font-weight:500;color:var(--ink-2)}
.nav nav a:hover{color:var(--em)}
.tg{width:40px;height:40px;border:1px solid var(--line);border-radius:50%;display:grid;place-items:center;cursor:pointer;background:transparent;color:var(--ink);transition:.18s}
.tg:hover{border-color:var(--em);color:var(--em)}
@media(max-width:820px){.nav nav{display:none}}
.hero{padding:60px 0 26px}
.hero .eye{color:var(--em);margin-bottom:18px}
h1.title{font-family:var(--f-disp);font-weight:400;font-size:clamp(38px,6.2vw,80px);line-height:1.0;letter-spacing:-1.6px}
h1.title .big{font-weight:600}h1.title em{font-style:italic;color:var(--sienna)}
.lede{font-family:var(--f-serif);font-size:clamp(17px,2.1vw,20px);line-height:1.55;color:var(--ink-2);max-width:600px;margin-top:22px}
.lede b{color:var(--ink);font-weight:500}
.cta{display:flex;gap:13px;flex-wrap:wrap;margin-top:24px}
.btn{font-family:var(--f-ui);font-weight:600;font-size:15px;padding:13px 24px;border-radius:3px;cursor:pointer;transition:.16s;border:1px solid transparent;display:inline-flex;align-items:center;gap:8px}
.btn.solid{background:var(--em);color:#f7f1e6;border-color:var(--em)}.btn.solid:hover{background:var(--em-ink)}
html[data-theme="ink"] .btn.solid{color:#15120c}
.btn.line{background:transparent;color:var(--ink);border-color:var(--line)}.btn.line:hover{border-color:var(--em);color:var(--em)}
.stripe{display:flex;gap:34px;flex-wrap:wrap;margin-top:34px;border-top:1px solid var(--line);padding-top:18px;font-size:14px;color:var(--ink-2)}
.stripe b{color:var(--em);font-weight:600;font-family:var(--f-disp);font-size:18px}
section{padding:44px 0}
.shead{margin-bottom:22px}.shead .k{color:var(--sienna);margin-bottom:10px}
.shead h2{font-family:var(--f-disp);font-weight:500;font-size:clamp(26px,4vw,40px);letter-spacing:-.8px}
.shead p{font-family:var(--f-serif);color:var(--ink-2);margin-top:6px;max-width:620px;font-size:17px}
.start{display:grid;grid-template-columns:1.05fr 1fr;gap:42px;border:1px solid var(--line);border-radius:4px;padding:28px;background:var(--paper-2)}
.start h3{font-family:var(--f-disp);font-weight:500;font-size:22px;margin-bottom:12px}
.steps{counter-reset:s;display:grid;gap:12px}
.steps li{list-style:none;display:flex;gap:13px;align-items:flex-start;font-family:var(--f-serif);font-size:16px;color:var(--ink-2)}
.steps li::before{counter-increment:s;content:counter(s);flex:none;width:27px;height:27px;border-radius:50%;border:1px solid var(--em);color:var(--em);font-family:var(--f-ui);font-weight:600;font-size:13px;display:grid;place-items:center;margin-top:2px}
.steps li b{color:var(--ink);font-weight:500;font-family:var(--f-ui)}
.pick .lbl{font-size:12px;letter-spacing:1.3px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-bottom:10px}
.ai-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.ai{display:flex;align-items:center;gap:8px;padding:10px 15px;border:1px solid var(--line);border-radius:3px;font-weight:600;font-size:14px;background:var(--paper);transition:.16s}
.ai:hover{border-color:var(--em);color:var(--em)}.ai i{width:8px;height:8px;border-radius:50%;background:var(--em)}
.ex{border:1px solid var(--line);border-radius:3px;padding:15px;background:var(--paper)}
.ex .t{font-size:11px;letter-spacing:1.1px;text-transform:uppercase;color:var(--sienna);font-weight:600;margin-bottom:7px}
.ex .q{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);white-space:pre-wrap;line-height:1.5}
@media(max-width:760px){.start{grid-template-columns:1fr;gap:26px;padding:20px}}
/* mode toggle */
.modebar{display:flex;justify-content:center;margin-bottom:18px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:4px;background:var(--paper);padding:4px;gap:4px}
.seg button{font-family:var(--f-ui);font-weight:600;font-size:15px;padding:10px 26px;border:none;border-radius:3px;background:transparent;color:var(--ink-2);cursor:pointer;transition:.16s;display:inline-flex;align-items:center;gap:8px}
.seg button.on{background:var(--em);color:#f7f1e6}
html[data-theme="ink"] .seg button.on{color:#15120c}
.controls{position:sticky;top:66px;z-index:40;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0}
.sb{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;font-family:var(--f-ui);font-size:15px;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:12px 14px 12px 42px;outline:none;transition:.16s}
.search input::placeholder{color:var(--ink-3)}.search input:focus{border-color:var(--em)}
.search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);stroke:var(--ink-3)}
.shown{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.frow{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:10px}
.glab{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-right:3px}
.chip{font-family:var(--f-ui);font-size:13px;font-weight:500;padding:7px 12px;border:1px solid var(--line);border-radius:3px;background:var(--paper);color:var(--ink-2);cursor:pointer;transition:.14s;white-space:nowrap}
.chip:hover{border-color:var(--em);color:var(--em)}.chip.on{background:var(--em);border-color:var(--em);color:#f7f1e6}
html[data-theme="ink"] .chip.on{color:#15120c}
.chip .n{opacity:.6;margin-left:5px;font-family:var(--f-mono);font-size:11px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;vertical-align:middle}.dot.text{background:var(--em)}.dot.image{background:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(322px,1fr));gap:14px;align-items:start;padding-top:22px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;display:flex;flex-direction:column;gap:10px;transition:.16s}
.card:hover{border-color:var(--em)}
.card .meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.card .ct{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--sienna);font-weight:600}
.badge{font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:2px;border:1px solid var(--line);color:var(--ink-3);letter-spacing:.3px}
.badge.ask{color:var(--blue);border-color:color-mix(in srgb,var(--blue) 36%,transparent)}
.badge.pic{color:var(--gold);border-color:color-mix(in srgb,var(--gold) 40%,transparent)}
.badge.sig{color:var(--em);border-color:color-mix(in srgb,var(--em) 36%,transparent)}
.card h3{font-family:var(--f-disp);font-weight:500;font-size:18px;line-height:1.25}
.card .yg{font-family:var(--f-serif);font-size:14.5px;color:var(--ink-2);line-height:1.45}
.card .yg b{color:var(--ink);font-weight:500;font-family:var(--f-ui);font-size:12px;letter-spacing:.3px}
.tagrow{display:flex;flex-wrap:wrap;gap:5px}
.ttag{font-size:11px;color:var(--ink-3);border:1px solid var(--line);padding:2px 8px;border-radius:2px}
.vars{display:flex;flex-wrap:wrap;gap:5px}
.var{font-family:var(--f-mono);font-size:11px;color:var(--gold);background:var(--em-soft);border:1px solid var(--line);padding:2px 7px;border-radius:2px}
.cbar{display:flex;gap:8px;margin-top:auto;padding-top:4px;flex-wrap:wrap}
.copy{flex:1;font-family:var(--f-ui);font-weight:600;font-size:13.5px;padding:11px;border-radius:3px;cursor:pointer;border:1px solid var(--em);background:var(--em);color:#f7f1e6;transition:.16s}
html[data-theme="ink"] .copy{color:#15120c}.copy:hover{background:var(--em-ink)}.copy.done{background:var(--gold);border-color:var(--gold);color:#2a1f08}
.view{font-family:var(--f-ui);font-weight:500;font-size:13px;padding:11px 15px;border-radius:3px;cursor:pointer;border:1px solid var(--line);background:transparent;color:var(--ink-2);transition:.16s}
.view:hover{border-color:var(--em);color:var(--em)}
.open{font-family:var(--f-ui);font-weight:600;font-size:13px;padding:11px 14px;border-radius:3px;cursor:pointer;border:1px solid var(--em);background:transparent;color:var(--em);transition:.16s}
.open:hover{background:var(--em-soft)}
.more{display:flex;justify-content:center;padding:30px 0 8px}
.empty{text-align:center;color:var(--ink-3);padding:60px 0;font-family:var(--f-serif);font-size:18px}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.tool{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;transition:.16s;display:block}
.tool:hover{border-color:var(--sienna)}
.tool h4{font-family:var(--f-disp);font-weight:500;font-size:18px;margin-bottom:5px;display:flex;align-items:center;gap:8px}
.tool h4 .a{color:var(--sienna);transition:.16s}.tool:hover h4 .a{transform:translate(3px,-3px)}
.tool p{font-family:var(--f-serif);font-size:14px;color:var(--ink-3);line-height:1.45}
.contact{border:1px solid var(--line);border-radius:4px;padding:34px;text-align:center;background:var(--paper-2)}
.contact h2{font-family:var(--f-disp);font-weight:500;font-size:clamp(26px,4vw,38px);letter-spacing:-.6px;margin-bottom:8px}
.contact p{font-family:var(--f-serif);font-size:18px;color:var(--ink-2);max-width:540px;margin:0 auto 22px}
.icons{display:flex;gap:12px;justify-content:center;margin-bottom:20px}
.ico{width:52px;height:52px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;color:var(--ink-2);transition:.16s;background:var(--paper)}
.ico:hover{border-color:var(--em);color:var(--em);transform:translateY(-3px)}.ico svg{width:22px;height:22px}
.fbk{display:inline-flex;align-items:center;gap:8px;font-family:var(--f-ui);font-weight:600;font-size:15px;padding:13px 26px;border-radius:3px;background:var(--em);color:#f7f1e6;border:1px solid var(--em);cursor:pointer}
html[data-theme="ink"] .fbk{color:#15120c}.fbk:hover{background:var(--em-ink)}
.wsh{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:20px}
.wbtn{font-family:var(--f-ui);font-weight:600;font-size:13px;padding:9px 15px;border-radius:3px;cursor:pointer;border:1px solid var(--line);background:var(--paper);color:var(--ink-2);transition:.16s}
.wbtn:hover{border-color:var(--em);color:var(--em)}
.note{font-family:var(--f-serif);font-size:14px;color:var(--ink-3);margin-top:18px;font-style:italic}
footer{border-top:1px solid var(--line);padding:30px 0 44px;text-align:center;color:var(--ink-3);font-size:14px}
footer .h{font-family:var(--f-disp);font-style:italic;color:var(--ink-2);font-size:17px}footer b{color:var(--ink-2)}
.modal{position:fixed;inset:0;z-index:90;display:none;align-items:center;justify-content:center;padding:20px;background:#0a0805aa;backdrop-filter:blur(4px)}
.modal.open{display:flex}
.sheet{width:min(720px,100%);max-height:88vh;overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:5px;padding:28px;position:relative}
.sheet .x{position:absolute;top:16px;right:16px;width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:transparent;color:var(--ink-2);cursor:pointer;font-size:16px}
.sheet h3{font-family:var(--f-disp);font-weight:500;font-size:25px;margin:8px 0 8px;letter-spacing:-.4px}
.sheet .yg{font-family:var(--f-serif);font-size:16px;color:var(--ink-2);margin-bottom:14px}
.lab{font-size:11px;letter-spacing:1.1px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin:14px 0 8px}
pre.full{white-space:pre-wrap;word-break:break-word;font-family:var(--f-mono);font-size:12.5px;line-height:1.6;color:var(--ink);background:var(--paper-2);border:1px solid var(--line);border-radius:3px;padding:16px;margin-bottom:14px}
#toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);opacity:0;z-index:100;background:var(--ink);color:var(--bg);padding:12px 20px;border-radius:3px;font-weight:600;font-size:14px;transition:.22s;pointer-events:none}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.reveal{opacity:0;transform:translateY(14px);animation:rise .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.reveal{animation:none;opacity:1;transform:none}*{scroll-behavior:auto!important}}
@media(max-width:760px){
 header.nav{backdrop-filter:none;-webkit-backdrop-filter:none;background:var(--bg)}
 .controls{position:static;backdrop-filter:none;-webkit-backdrop-filter:none;background:transparent}
 .frow{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px;scrollbar-width:none}
 .frow::-webkit-scrollbar{display:none}
 .chip,.seg button{flex:0 0 auto}
 .sheet{padding:20px}
 pre.full{font-size:13px}
}
@media(max-width:560px){.grid{grid-template-columns:1fr}.seg button{padding:10px 18px}.cbar .copy{flex:1 0 100%}}
</style>
</head>
<body>
<a id="top"></a>
<header class="nav"><div class="wrap row">
  <a class="brand" href="#top"><span class="seal">P</span>__BRAND__</a>
  <nav><a href="#start">Start here</a><a href="#library">Library</a><a href="#tools">Tools</a><a href="#contact">Contact</a></nav>
  <button class="tg" id="theme" aria-label="Toggle day / ink mode" title="Day / Ink"></button>
</div></header>

<section class="hero"><div class="wrap">
  <div class="sc eye reveal">Free · teachers &amp; students · JEE · NEET · Olympiad · Boards</div>
  <h1 class="title reveal" style="animation-delay:.05s"><span class="big">__COUNT__+</span> premium prompts that<br>think <em>with</em> you, not for you.</h1>
  <p class="lede reveal" style="animation-delay:.12s">Master prompts for every teacher and student. Many <b>ask you a few questions first</b>, then deliver a premium, exam-accurate answer. <b>Attach a photo</b> of any question and they solve it — step by step. Every answer comes <b>signed</b>, so students can find their teacher.</p>
  <div class="cta reveal" style="animation-delay:.18s"><a class="btn solid" href="#library">Open the library</a><a class="btn line" href="#start">New to AI? Start here →</a></div>
  <div class="stripe reveal" style="animation-delay:.24s"><span><b>__COUNT__+</b> prompts</span><span><b>2</b> modes</span><span><b>4</b> tracks</span><span><b>Photo</b>-aware</span><span><b>Free</b> forever</span></div>
</div></section>

<section id="start"><div class="wrap">
  <div class="shead"><div class="sc k">Start here · 60 seconds</div><h2>Two modes. Pick yours.</h2>
    <p>👩‍🏫 <b>Teacher</b> — make solutions, mock papers, lessons, doubt-clinics. 🎓 <b>Student</b> — get a tutor, solve doubts from a photo, plan your prep.</p></div>
  <div class="start">
    <div><h3>Four small steps.</h3>
      <ol class="steps">
        <li><div><b>Open a free AI tool</b> — pick one on the right.</div></li>
        <li><div><b>Choose Teacher or Student</b>, then your track &amp; subject below.</div></li>
        <li><div><b>Copy a prompt, paste it</b>, and answer its questions (or attach your question's photo).</div></li>
        <li><div><b>Get a premium answer</b> — signed so students can reach their teacher.</div></li>
      </ol>
    </div>
    <div class="pick"><div class="lbl">Open a free AI tool</div>
      <div class="ai-row">
        <a class="ai" href="https://chatgpt.com" target="_blank" rel="noopener"><i></i>ChatGPT</a>
        <a class="ai" href="https://claude.ai" target="_blank" rel="noopener"><i></i>Claude</a>
        <a class="ai" href="https://gemini.google.com" target="_blank" rel="noopener"><i></i>Gemini</a>
      </div>
      <div class="ex"><div class="t">What "asks-first" feels like</div><div class="q">You: *copy a tutor prompt*
AI: "Before I solve — what's your class &amp; target exam,
and where exactly are you stuck? (1/4)"
You: answer · AI guides you to the answer.</div></div>
    </div>
  </div>
</div></section>

<section id="library"><div class="wrap">
  <div class="shead"><div class="sc k">The Library</div><h2>__COUNT__+ premium prompts</h2>
    <p>Switch modes, choose a track &amp; subject, or search. Look for the <span style="color:var(--blue);font-weight:600">asks first</span> and <span style="color:var(--gold);font-weight:600">photo</span> badges.</p></div>
  <div class="modebar"><div class="seg" id="modeSeg"></div></div>
</div></section>

<div class="controls"><div class="wrap">
  <div class="sb">
    <div class="search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search prompts — mock test, doubt, study plan, integration, NCERT…" autocomplete="off"/></div>
    <span class="shown" id="shown"></span>
  </div>
  <div class="frow"><span class="glab">Track</span><span id="trackChips" style="display:contents"></span></div>
  <div class="frow"><span class="glab">Subject</span><span id="subChips" style="display:contents"></span></div>
  <div class="frow"><span class="glab">Type</span><span id="catChips" style="display:contents"></span>
    <span class="glab" style="margin-left:8px">Format</span>
    <span class="chip tf on" data-type="all" onclick="setType('all',this)">All</span>
    <span class="chip tf" data-type="text" onclick="setType('text',this)"><span class="dot text"></span> Text</span>
    <span class="chip tf" data-type="image" onclick="setType('image',this)"><span class="dot image"></span> Photo</span>
    <span class="chip af" onclick="toggleAsk(this)">💬 Asks first</span>
  </div>
  <div class="frow"><span class="glab">Open in</span><span id="aiChips" style="display:contents"></span><span class="glab" style="opacity:.7;margin-left:6px;text-transform:none;letter-spacing:0">↳ the Open ↗ button copies &amp; opens this AI</span></div>
</div></div>

<div class="wrap"><div class="grid" id="grid"></div><div class="more" id="more"></div></div>

<section id="tools"><div class="wrap">
  <div class="shead"><div class="sc k">More free tools</div><h2>Other projects by __AUTHOR__</h2><p>More free, no-login resources for teachers and students.</p></div>
  <div class="tools" id="toolGrid"></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="contact">
    <div class="sc k" style="color:var(--sienna);margin-bottom:12px">Stay in touch</div>
    <h2>Feedback, problems or appreciation?</h2>
    <p>I'd love to hear how this helps — and what to add next. Tap to reach me.</p>
    <div class="icons" id="icons"></div>
    <div><a class="fbk" id="fbk"></a></div>
    <div class="wsh" id="wsh"></div>
    <p class="note">Every prompt signs each AI answer with my name and this site — so students and parents can always find their teacher.</p>
  </div>
</div></section>

<footer><div class="wrap"><span class="h">Made for teachers &amp; students, everywhere.</span><br><br>
  <b>__BRAND__</b> · __COUNT__+ premium prompts · Built __BUILD__ · Created &amp; curated by <b>__AUTHOR__</b> · __ROLE__<br>Free to share — please keep the credit.</div></footer>

<div class="modal" id="modal"><div class="sheet" id="sheet"></div></div>
<div id="toast">Copied!</div>

<script id="DATA" type="application/json">__DATA__</script>
<script id="CFG" type="application/json">__CFG__</script>
<script>
const P=JSON.parse(document.getElementById('DATA').textContent);
const C=JSON.parse(document.getElementById('CFG').textContent);
const $=s=>document.querySelector(s);
const esc=s=>(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const PAGE=48;
let st={mode:'Teacher',track:'all',sub:'all',cat:'all',type:'all',ask:false,q:'',shown:PAGE,ai:'chatgpt'};
try{const a=localStorage.getItem('ps-ai');if(a)st.ai=a;}catch(e){}
const AINAME={chatgpt:'ChatGPT',claude:'Claude',gemini:'Gemini'};
function buildAI(){const box=document.getElementById('aiChips');if(!box)return;box.innerHTML='';['chatgpt','claude','gemini'].forEach(a=>{const s=document.createElement('span');s.className='chip'+(st.ai===a?' on':'');s.textContent=AINAME[a];s.onclick=()=>{st.ai=a;try{localStorage.setItem('ps-ai',a)}catch(e){}buildAI();};box.appendChild(s);});}
function openAI(text){copyText(text);const ai=st.ai||'chatgpt';const enc=encodeURIComponent(text);let url;
 if(ai==='chatgpt')url=enc.length<5000?'https://chatgpt.com/?q='+enc:'https://chatgpt.com/';
 else if(ai==='claude')url=enc.length<5000?'https://claude.ai/new?q='+enc:'https://claude.ai/new';
 else url='https://gemini.google.com/app';
 window.open(url,'_blank','noopener');
 toast('Copied — opening '+AINAME[ai]+'. Just paste (Ctrl/Cmd+V) if it is not pre-filled.');}

const SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/></svg>';
const MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 109.8 9.8z"/></svg>';
const tb=$('#theme');
function applyTheme(t){document.documentElement.dataset.theme=t;tb.innerHTML=t==='day'?MOON:SUN;try{localStorage.setItem('ps-theme',t)}catch(e){}}
applyTheme((()=>{try{const v=localStorage.getItem('ps-theme');return (v==='day'||v==='ink')?v:'day'}catch(e){return 'day'}})());
tb.onclick=()=>applyTheme(document.documentElement.dataset.theme==='day'?'ink':'day');
function copyText(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(()=>fb(t));}return Promise.resolve(fb(t));}
function fb(t){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.top='-9999px';document.body.appendChild(a);a.focus();a.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(a);}
let tT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(tT);tT=setTimeout(()=>t.classList.remove('show'),1500);}

const ICON={mail:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>',
 wa:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3a9 9 0 00-7.7 13.7L3 21l4.5-1.2A9 9 0 1012 3z"/></svg>',
 ig:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>'};
(function(){const c=C.contact;const links={mail:'mailto:'+c.email+'?subject='+encodeURIComponent('Feedback — '+C.brand),wa:'https://wa.me/'+c.wa_num,ig:'https://instagram.com/'+c.insta};
 const titles={mail:'Email me',wa:'WhatsApp me',ig:'Instagram'};const box=$('#icons');
 ['mail','wa','ig'].forEach(k=>{const a=document.createElement('a');a.className='ico';a.href=links[k];a.setAttribute('aria-label',titles[k]);a.title=titles[k];if(k!=='mail'){a.target='_blank';a.rel='noopener';}a.innerHTML=ICON[k];box.appendChild(a);});
 const f=$('#fbk');if(C.form){f.href=C.form;f.target='_blank';f.rel='noopener';}else{f.href=links.mail;}f.textContent='📝 Send feedback';
 const ws=$('#wsh');Object.keys(C.wa).forEach(k=>{const b=document.createElement('button');b.className='wbtn';b.textContent='Copy WhatsApp: '+k.replace(/ \(.*\)/,'');b.onclick=()=>{copyText(C.wa[k]);toast('WhatsApp message copied');};ws.appendChild(b);});})();
(function(){const g=$('#toolGrid');C.tools.forEach(t=>{const a=document.createElement('a');a.className='tool';a.href=t.url;a.target='_blank';a.rel='noopener';a.innerHTML='<h4>'+esc(t.name)+' <span class="a">↗</span></h4><p>'+esc(t.desc)+'</p>';g.appendChild(a);});})();

const inMode=p=>p.mode===st.mode;
const cnt=f=>P.filter(f).length;
function buildMode(){const s=$('#modeSeg');s.innerHTML='';C.modes.forEach(m=>{const b=document.createElement('button');b.className=m===st.mode?'on':'';
  b.innerHTML=(m==='Teacher'?'👩‍🏫 ':'🎓 ')+m+' <span style="opacity:.6;font-weight:500">'+cnt(p=>p.mode===m)+'</span>';
  b.onclick=()=>{st.mode=m;st.track='all';st.sub='all';st.cat='all';st.shown=PAGE;buildMode();buildFacets();render();};s.appendChild(b);});}
function chip(label,on,onclick,n){const s=document.createElement('span');s.className='chip'+(on?' on':'');s.innerHTML=esc(label)+(n!=null?' <span class="n">'+n+'</span>':'');s.onclick=onclick;return s;}
function buildFacets(){
 const tracks=C.trackOrder.filter(t=>cnt(p=>inMode(p)&&p.track===t)>0);
 const tc=$('#trackChips');tc.innerHTML='';tc.appendChild(chip('All',st.track==='all',()=>{st.track='all';st.sub='all';st.shown=PAGE;buildFacets();render();},cnt(inMode)));
 tracks.forEach(t=>tc.appendChild(chip(C.trackLabel[t]||t,st.track===t,()=>{st.track=t;st.sub='all';st.shown=PAGE;buildFacets();render();},cnt(p=>inMode(p)&&p.track===t))));
 const subF=p=>inMode(p)&&(st.track==='all'||p.track===st.track);
 const subs=[...new Set(P.filter(subF).map(p=>p.subject))].sort();
 const sc=$('#subChips');sc.innerHTML='';sc.appendChild(chip('All',st.sub==='all',()=>{st.sub='all';st.shown=PAGE;buildFacets();render();},cnt(subF)));
 subs.forEach(su=>sc.appendChild(chip(su,st.sub===su,()=>{st.sub=su;st.shown=PAGE;buildFacets();render();},cnt(p=>subF(p)&&p.subject===su))));
 const catF=p=>subF(p)&&(st.sub==='all'||p.subject===st.sub);
 const cats=[...new Set(P.filter(catF).map(p=>p.category))].sort();
 const cc=$('#catChips');cc.innerHTML='';cc.appendChild(chip('All',st.cat==='all',()=>{st.cat='all';st.shown=PAGE;buildFacets();render();},cnt(catF)));
 cats.forEach(ca=>cc.appendChild(chip(ca,st.cat===ca,()=>{st.cat=ca;st.shown=PAGE;buildFacets();render();},cnt(p=>catF(p)&&p.category===ca))));
}
function setType(t,el){st.type=t;st.shown=PAGE;document.querySelectorAll('.tf').forEach(x=>x.classList.toggle('on',x===el));render();}
function toggleAsk(el){st.ask=!st.ask;st.shown=PAGE;el.classList.toggle('on',st.ask);render();}
function match(p){
 if(!inMode(p))return false;
 if(st.track!=='all'&&p.track!==st.track)return false;
 if(st.sub!=='all'&&p.subject!==st.sub)return false;
 if(st.cat!=='all'&&p.category!==st.cat)return false;
 if(st.type!=='all'&&p.output_type!==st.type)return false;
 if(st.ask&&!p.interactive)return false;
 if(st.q){const h=(p.title+' '+p.category+' '+p.track+' '+p.subject+' '+(p.what_you_get||'')+' '+p.prompt+' '+(p.variables||[]).join(' ')).toLowerCase();return st.q.split(/\s+/).every(w=>h.includes(w));}
 return true;
}
const grid=$('#grid');
function render(){
 const items=P.filter(match);
 $('#shown').textContent=Math.min(st.shown,items.length)+' / '+items.length+' shown';
 grid.innerHTML='';
 if(!items.length){grid.innerHTML='<div class="empty">No prompts match. Try another track, subject or word.</div>';$('#more').innerHTML='';return;}
 const fr=document.createDocumentFragment();
 items.slice(0,st.shown).forEach((p,i)=>{
  const card=document.createElement('article');card.className='card';
  const vars=(p.variables||[]).slice(0,5).map(v=>'<span class="var">'+esc(v)+'</span>').join('');
  const badges=(p.interactive?'<span class="badge ask">💬 asks first</span>':'')+(p.output_type==='image'?'<span class="badge pic">🖼 photo</span>':'')+'<span class="badge sig">✍ signed</span>';
  card.innerHTML='<div class="meta"><span class="ct">'+esc(p.track)+' · '+esc(p.subject)+'</span></div>'+
   '<div class="tagrow">'+badges+'</div>'+
   '<h3>'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg"><b>YOU GET — </b>'+esc(p.what_you_get)+'</p>':'')+
   '<div class="meta"><span class="ct" style="color:var(--ink-3)">'+esc(p.category)+'</span></div>'+
   (vars?'<div class="vars">'+vars+'</div>':'')+
   '<div class="cbar"><button class="copy">Copy</button><button class="open">Open ↗</button><button class="view">View</button></div>';
  const cp=card.querySelector('.copy');
  cp.onclick=()=>{copyText(p.prompt);cp.classList.add('done');cp.textContent='✓ Copied!';toast('Prompt copied — paste it into your AI');setTimeout(()=>{cp.classList.remove('done');cp.textContent='Copy';},1600);};
  card.querySelector('.open').onclick=()=>openAI(p.prompt);
  card.querySelector('.view').onclick=()=>openModal(p);
  if(i<9){card.classList.add('reveal');card.style.animationDelay=(i*0.03)+'s';}
  fr.appendChild(card);
 });
 grid.appendChild(fr);
 const rem=items.length-st.shown;
 $('#more').innerHTML = rem>0 ? '' : '';
 if(rem>0){const b=document.createElement('button');b.className='btn line';b.textContent='Show more ('+rem+' more)';b.onclick=()=>{st.shown+=PAGE;render();};$('#more').innerHTML='';$('#more').appendChild(b);}
}
const modal=$('#modal');
function openModal(p){
 const vars=(p.variables||[]).map(v=>'<span class="var">'+esc(v)+'</span>').join(' ');
 const lvls=(p.level||[]).map(l=>'<span class="ttag">'+esc(l)+'</span>').join(' ');
 const badges=(p.interactive?'<span class="badge ask">💬 asks you first</span> ':'')+(p.output_type==='image'?'<span class="badge pic">🖼 photo-aware</span> ':'')+'<span class="badge sig">✍ auto-signed</span>';
 $('#sheet').innerHTML='<button class="x" onclick="closeModal()" aria-label="Close">✕</button>'+
  '<div class="meta"><span class="ct">'+esc(p.mode)+' · '+esc(p.track)+' · '+esc(p.subject)+'</span></div>'+
  '<div class="tagrow" style="margin:6px 0">'+badges+'</div>'+
  '<h3>'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg">'+esc(p.what_you_get)+'</p>':'')+
  '<div class="lab">'+esc(p.category)+(lvls?' · best for':'')+'</div>'+(lvls?'<div class="tagrow">'+lvls+'</div>':'')+
  (vars?'<div class="lab">Fill in these</div><div class="vars">'+vars+'</div>':'')+
  '<div class="lab">The prompt</div><pre class="full">'+esc(p.prompt)+'</pre>'+
  '<div class="cbar"><button class="copy" id="mc" style="flex:1">Copy prompt</button><button class="open" id="mo">Open ↗ in '+AINAME[st.ai||'chatgpt']+'</button></div>';
 $('#mc').onclick=()=>{copyText(p.prompt);toast('Prompt copied');const b=$('#mc');b.classList.add('done');b.textContent='✓ Copied!';setTimeout(()=>{b.classList.remove('done');b.textContent='Copy prompt';},1600);};
 $('#mo').onclick=()=>openAI(p.prompt);
 modal.classList.add('open');document.body.style.overflow='hidden';
}
function closeModal(){modal.classList.remove('open');document.body.style.overflow='';}
modal.onclick=e=>{if(e.target===modal)closeModal();};
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
let qt;$('#q').addEventListener('input',e=>{clearTimeout(qt);qt=setTimeout(()=>{st.q=e.target.value.trim().toLowerCase();st.shown=PAGE;render();},110);});
buildMode();buildFacets();buildAI();render();
</script>
</body>
</html>
"""

out=(TEMPLATE.replace("__BRAND__",esc(BRAND)).replace("__AUTHOR__",esc(AUTHOR)).replace("__ROLE__",esc(ROLE))
 .replace("__BUILD__",BUILD).replace("__COUNT__",str(COUNT))
 .replace("__DATA__",jsemb(prompts)).replace("__CFG__",jsemb(CONFIG)))
open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(out)

# prompt-pack.md
md=[f"# {BRAND}","",f"_{COUNT}+ premium AI prompts for teachers & students — curated by {AUTHOR}. Built {BUILD}._","",
 "Works with ChatGPT, Claude or Gemini. Many prompts ask you questions first; many accept a photo of your question. Every prompt signs its answer with a link back to this studio.",""]
by={}
for p in prompts: by.setdefault((p["mode"],p["track"],p["subject"]),[]).append(p)
for key in sorted(by.keys()):
 m,t,s=key
 md.append(f"\n## {m} · {t} · {s}  ({len(by[key])})\n")
 for p in by[key]:
  md.append(f"### {p['title']}")
  tags=[]
  if p.get("interactive"): tags.append("asks-first")
  if p.get("output_type")=="image": tags.append("photo")
  if tags: md.append("_"+", ".join(tags)+"_")
  if p.get("what_you_get"): md.append(f"You get: {p['what_you_get']}")
  if p.get("variables"): md.append("Fill in: "+", ".join(f"`{v}`" for v in p["variables"]))
  md.append("\n```\n"+p["prompt"].strip()+"\n```\n")
open(os.path.join(HERE,"prompt-pack.md"),"w",encoding="utf-8").write("\n".join(md))

# WHATSAPP-MESSAGES.txt
wt=["="*60,f"  {BRAND} — WhatsApp messages (copy & paste)","="*60,""]
for k,v in WA.items(): wt+=[f"\n----- {k} -----\n",v,""]
wt+=["\nLive link (in every message):","  "+SITE_URL,"Contacts are click-only on the site and never shown as text."]
open(os.path.join(HERE,"WHATSAPP-MESSAGES.txt"),"w",encoding="utf-8").write("\n".join(wt))

print(f"Built index.html ({os.path.getsize(os.path.join(HERE,'index.html'))//1024} KB) · {COUNT} prompts")
