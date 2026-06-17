#!/usr/bin/env python3
"""Build 'Prompt Studio for Teachers' — Ivory Editorial edition.
Run: python3 build_site.py  ->  index.html, prompt-pack.md, WHATSAPP-MESSAGES.txt
"""
import json, html, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
prompts = json.load(open(os.path.join(HERE, "data", "prompts.json"), encoding="utf-8"))

# ---------------- CONFIG ----------------
AUTHOR="Indrajeet Yadav"; ROLE="Maths Faculty"; BRAND="Prompt Studio for Teachers"
TAGLINE="Free AI prompts that quietly do a teacher's busywork."
BUILD=datetime.date.today().isoformat()
SITE_URL="https://yosoyun.github.io/ai-prompt-library-for-teachers/"

# Contacts are used ONLY inside click links (never shown as text).
CONTACT={"email":"indrajeetsirallen@gmail.com","wa_num":"918072965053","insta":"indrajeetsirallen"}
# Paste a Google Form URL when ready (empty -> Send feedback opens an email).
FEEDBACK_FORM_URL=""

TOOLS=[
 {"name":"Maths Prompt Studio","desc":"136+ AI prompts for maths teachers — solutions, papers, worksheets, DPPs.","url":"https://yosoyun.github.io/math-prompt-studio/"},
 {"name":"Ranker Masterbooks","desc":"ARC & LIMITS — 200 original multi-method problems, Python-verified.","url":"https://yosoyun.github.io/ranker-masterbooks/"},
 {"name":"Andreescu Library","desc":"A searchable guide to every book by Titu Andreescu.","url":"https://yosoyun.github.io/andreescu-library/"},
 {"name":"LIMITS Masterbook","desc":"100 ranker-level limit problems (JEE Advanced / Olympiad).","url":"https://limits-masterbook.vercel.app"},
]

CATEGORY_ORDER=["Solutions & Worked Examples","Practice, DPP & Tests","Question Papers & Assessment",
 "Concepts, Proofs & Theory","Doubt-Solving & Remedial","Visual & Diagram Maths","Lesson Planning & Notes",
 "Student Feedback & Mentoring","WhatsApp & Parent Communication","Content & Social Media",
 "AI Productivity & Workflow","Prompt-Writing & Meta"]
CAT_DESC={
 "Solutions & Worked Examples":"Step-by-step solutions, multi-method answers, worked pages.",
 "Practice, DPP & Tests":"DPPs, daily practice, drills and graded assignments.",
 "Question Papers & Assessment":"Exam papers, board tests, answer keys and rubrics.",
 "Concepts, Proofs & Theory":"Explain concepts, prove theorems, build intuition.",
 "Doubt-Solving & Remedial":"Fix misconceptions and repair weak foundations.",
 "Visual & Diagram Maths":"Graphs, diagrams, figures and visual explanations.",
 "Lesson Planning & Notes":"Lesson plans, revision sheets, notes and workflow.",
 "Student Feedback & Mentoring":"Feedback, mentoring and personalised guidance.",
 "WhatsApp & Parent Communication":"Parent updates and clean WhatsApp-ready messages.",
 "Content & Social Media":"YouTube, Instagram and post ideas for educators.",
 "AI Productivity & Workflow":"Summaries, custom instructions and time-savers.",
 "Prompt-Writing & Meta":"Build and sharpen your own prompts."}
LEVELS=["School (6–10)","Boards (11–12)","JEE / NEET","Olympiad","Any"]

def varlist(v):
    if isinstance(v,list): return [str(x).strip() for x in v if str(x).strip()]
    if not v: return []
    import re; return [x.strip() for x in re.split(r"[,\n]",str(v)) if x.strip()]

norm=[]
for i,p in enumerate(prompts,1):
    cat=p.get("category","AI Productivity & Workflow")
    if cat not in CATEGORY_ORDER: cat="AI Productivity & Workflow"
    lv=p.get("level") or ["Any"]
    if isinstance(lv,str): lv=[lv]
    lv=[x for x in lv if x in LEVELS] or ["Any"]
    norm.append({"id":p.get("id",f"P{i:03d}"),"title":(p.get("title") or "Untitled").strip(),
      "category":cat,"level":lv,"output_type":"image" if str(p.get("output_type","")).lower()=="image" else "text",
      "use_case":(p.get("use_case") or "").strip(),"what_you_get":(p.get("what_you_get") or p.get("use_case") or "").strip(),
      "variables":varlist(p.get("variables",[])),"prompt":(p.get("prompt") or "").strip(),"tool":(p.get("tool") or "Any").strip()})
prompts=norm; COUNT=len(prompts)
counts={c:0 for c in CATEGORY_ORDER}
for p in prompts: counts[p["category"]]+=1
used=[c for c in CATEGORY_ORDER if counts[c]>0]

WA={
"Invite (English)":"🎓 *"+BRAND+"*  —  free AI prompts for teachers\n\n"+str(COUNT)+" ready-to-use, copy-paste prompts that save hours every day — solutions, DPPs, question papers, doubt-solving, lesson plans, parent & WhatsApp messages and more.\n\n✅ 100% copy-paste. Works on ChatGPT, Claude or Gemini (free versions too).\n🧩 Open → pick a prompt → fill the [BLANKS] → paste into the AI.\n\n👉 "+SITE_URL+"\n\nMade for teachers, by "+AUTHOR+".",
"How to use it daily (English)":"📌 *How to use "+BRAND+" every day*\n\n1️⃣ Open the link & bookmark it on your phone.\n2️⃣ Tap *Start here* once to see a 60-second example.\n3️⃣ Pick a category (DPP, Question Paper, Doubt-Solving…) or search.\n4️⃣ Tap *Copy*, paste into ChatGPT / Claude / Gemini.\n5️⃣ Replace the [BRACKETS] — e.g. [TOPIC] → Integration, [GRADE] → Class 12.\n6️⃣ Send. Every answer is signed so students can find you.\n\n👉 "+SITE_URL,
"Invite (Hindi)":"🎓 *"+BRAND+"* — शिक्षकों के लिए मुफ़्त AI प्रॉम्प्ट\n\nरोज़ घंटों बचाने वाले "+str(COUNT)+" तैयार प्रॉम्प्ट — हल, DPP, प्रश्न-पत्र, डाउट सॉल्विंग, लेसन प्लान, पैरेंट/WhatsApp मैसेज और भी बहुत कुछ।\n\n✅ पूरी तरह कॉपी-पेस्ट। ChatGPT, Claude या Gemini पर चलता है।\n🧩 खोलें → प्रॉम्प्ट चुनें → [BRACKETS] भरें → AI में पेस्ट करें।\n\n👉 "+SITE_URL+"\n\nशिक्षकों के लिए — "+AUTHOR+" द्वारा।"}

def esc(s): return html.escape(s or "",quote=True)
def jsemb(o): return json.dumps(o,ensure_ascii=False).replace("</","<\\/")
CONFIG={"brand":BRAND,"author":AUTHOR,"role":ROLE,"site":SITE_URL,"count":COUNT,
 "contact":CONTACT,"form":FEEDBACK_FORM_URL,"tools":TOOLS,"catOrder":used,
 "catDesc":{c:CAT_DESC[c] for c in used},"levels":LEVELS,"wa":WA}

TEMPLATE=r"""<!DOCTYPE html>
<html lang="en" data-theme="day">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="description" content="__COUNT__ free, copy-paste AI prompts for teachers — solutions, DPPs, question papers, doubt-solving, lesson plans and more. Works with ChatGPT, Claude and Gemini."/>
<meta name="theme-color" content="#f7f1e6"/>
<title>__BRAND__ · __COUNT__ free AI prompts for teachers</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,900;1,9..144,400;1,9..144,500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
 --bg:#f7f1e6; --paper:#fffdf7; --paper-2:#fbf6ec;
 --ink:#211d16; --ink-2:#4a4338; --ink-3:#6f685a;
 --line:#211d1622; --line-2:#211d1610;
 --em:#1c4a3a; --em-ink:#123528; --em-soft:#1c4a3a14;
 --sienna:#9a4a2a; --gold:#a9772a;
 --f-disp:"Fraunces",Georgia,serif; --f-serif:"Newsreader",Georgia,serif;
 --f-ui:"Hanken Grotesk",-apple-system,sans-serif; --f-mono:"JetBrains Mono",ui-monospace,monospace;
 --maxw:1140px;
}
html[data-theme="ink"]{
 --bg:#15120c; --paper:#1e1a12; --paper-2:#241f15;
 --ink:#ece3d2; --ink-2:#b6ab95; --ink-3:#8a8070;
 --line:#ffffff1f; --line-2:#ffffff10;
 --em:#7cc6a3; --em-ink:#bfe7d4; --em-soft:#7cc6a31a; --sienna:#df9468; --gold:#e2b667;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--f-ui);font-size:16px;line-height:1.55;
 background-image:radial-gradient(var(--line-2) 1px,transparent 1px);background-size:22px 22px;
 -webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
::selection{background:var(--em);color:var(--bg)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 40px}
@media(max-width:640px){.wrap{padding:0 22px}}
.sc{font-family:var(--f-ui);font-size:12px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase}
.serif{font-family:var(--f-serif)}

/* nav */
header.nav{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 88%,transparent);
 backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav .row{display:flex;align-items:center;gap:20px;height:68px}
.brand{display:flex;align-items:center;gap:11px;font-family:var(--f-disp);font-weight:600;font-size:20px;letter-spacing:-.3px}
.brand .seal{width:34px;height:34px;border:1.5px solid var(--em);border-radius:50%;display:grid;place-items:center;
 font-family:var(--f-disp);font-style:italic;color:var(--em);font-size:17px}
.nav nav{display:flex;gap:28px;margin-left:auto;font-size:14px;font-weight:500;color:var(--ink-2)}
.nav nav a:hover{color:var(--em)}
.tg{width:40px;height:40px;border:1px solid var(--line);border-radius:50%;display:grid;place-items:center;cursor:pointer;
 background:transparent;color:var(--ink);transition:.18s}
.tg:hover{border-color:var(--em);color:var(--em)}
@media(max-width:760px){.nav nav{display:none}}

/* hero */
.hero{padding:64px 0 30px}
.hero .eye{color:var(--em);margin-bottom:20px}
.hgrid{display:grid;grid-template-columns:1.5fr 1fr;gap:52px;align-items:end}
h1.title{font-family:var(--f-disp);font-weight:400;font-size:clamp(40px,6.4vw,84px);line-height:.99;letter-spacing:-1.6px}
h1.title .big{font-weight:600}
h1.title em{font-style:italic;color:var(--sienna)}
.rule{height:1px;background:var(--line);margin:28px 0 22px}
.lede{font-family:var(--f-serif);font-size:clamp(17px,2.1vw,20px);line-height:1.55;color:var(--ink-2);max-width:440px}
.lede b{color:var(--ink);font-weight:500}
.cta{display:flex;gap:13px;flex-wrap:wrap;margin-top:26px}
.btn{font-family:var(--f-ui);font-weight:600;font-size:15px;padding:13px 24px;border-radius:3px;cursor:pointer;transition:.16s;border:1px solid transparent;display:inline-flex;align-items:center;gap:8px}
.btn.solid{background:var(--em);color:#f7f1e6;border-color:var(--em)}
.btn.solid:hover{background:var(--em-ink)}
html[data-theme="ink"] .btn.solid{color:#15120c}
.btn.line{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.line:hover{border-color:var(--em);color:var(--em)}
.aside{border-left:1px solid var(--line);padding-left:30px}
.aside .num{font-family:var(--f-disp);font-size:104px;font-weight:600;line-height:.78;color:var(--em)}
.aside .nlab{font-size:13px;letter-spacing:.8px;text-transform:uppercase;color:var(--ink-3);margin:10px 0 24px;font-weight:600}
.mini{background:var(--paper);border:1px solid var(--line);padding:16px 18px;margin-bottom:12px;border-radius:3px}
.mini .ct{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--sienna);font-weight:600}
.mini h4{font-family:var(--f-disp);font-weight:500;font-size:18px;margin:6px 0 4px;line-height:1.2}
.mini p{font-family:var(--f-serif);font-size:14px;color:var(--ink-3)}
.stripe{display:flex;gap:34px;flex-wrap:wrap;margin-top:34px;border-top:1px solid var(--line);padding-top:18px;font-size:14px;color:var(--ink-2)}
.stripe b{color:var(--em);font-weight:600}
@media(max-width:820px){.hgrid{grid-template-columns:1fr;gap:36px}.aside{border-left:0;padding-left:0;border-top:1px solid var(--line);padding-top:28px}}

section{padding:48px 0}
.shead{margin-bottom:26px}
.shead .k{color:var(--sienna);margin-bottom:10px}
.shead h2{font-family:var(--f-disp);font-weight:500;font-size:clamp(28px,4vw,42px);letter-spacing:-.8px}
.shead p{font-family:var(--f-serif);color:var(--ink-2);margin-top:6px;max-width:560px;font-size:17px}

/* start */
.start{display:grid;grid-template-columns:1.05fr 1fr;gap:44px;border:1px solid var(--line);border-radius:4px;padding:30px;background:var(--paper-2)}
.start h3{font-family:var(--f-disp);font-weight:500;font-size:23px;margin-bottom:12px}
.steps{counter-reset:s;display:grid;gap:13px}
.steps li{list-style:none;display:flex;gap:13px;align-items:flex-start;font-family:var(--f-serif);font-size:16px;color:var(--ink-2)}
.steps li::before{counter-increment:s;content:counter(s);flex:none;width:27px;height:27px;border-radius:50%;border:1px solid var(--em);
 color:var(--em);font-family:var(--f-ui);font-weight:600;font-size:13px;display:grid;place-items:center;margin-top:2px}
.steps li b{color:var(--ink);font-weight:500;font-family:var(--f-ui)}
.pick .lbl{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-bottom:10px}
.ai-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.ai{display:flex;align-items:center;gap:8px;padding:10px 15px;border:1px solid var(--line);border-radius:3px;font-weight:600;font-size:14px;background:var(--paper);transition:.16s}
.ai:hover{border-color:var(--em);color:var(--em)}
.ai i{width:8px;height:8px;border-radius:50%;background:var(--em)}
.ex{border:1px solid var(--line);border-radius:3px;padding:15px;background:var(--paper)}
.ex .t{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--sienna);font-weight:600;margin-bottom:7px}
.ex .q{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);white-space:pre-wrap;line-height:1.5}
@media(max-width:760px){.start{grid-template-columns:1fr;gap:28px;padding:22px}}

/* category shelves */
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:12px}
.cat{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;cursor:pointer;transition:.16s;position:relative}
.cat:hover{border-color:var(--em);background:var(--paper-2)}
.cat .ct{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--sienna);font-weight:600}
.cat h4{font-family:var(--f-disp);font-weight:500;font-size:18px;margin:7px 0 5px;line-height:1.2;padding-right:30px}
.cat p{font-family:var(--f-serif);font-size:13.5px;color:var(--ink-3);line-height:1.4}
.cat .n{position:absolute;top:16px;right:16px;font-family:var(--f-mono);font-size:12px;color:var(--ink-3)}

/* controls */
.controls{position:sticky;top:68px;z-index:40;background:color-mix(in srgb,var(--bg) 90%,transparent);
 backdrop-filter:blur(8px);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0}
.sb{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;font-family:var(--f-ui);font-size:15px;color:var(--ink);background:var(--paper);
 border:1px solid var(--line);border-radius:3px;padding:12px 14px 12px 42px;outline:none;transition:.16s}
.search input::placeholder{color:var(--ink-3)}
.search input:focus{border-color:var(--em)}
.search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);stroke:var(--ink-3)}
.shown{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.frow{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:11px}
.glab{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-right:3px}
.chip{font-family:var(--f-ui);font-size:13px;font-weight:500;padding:7px 12px;border:1px solid var(--line);border-radius:3px;
 background:var(--paper);color:var(--ink-2);cursor:pointer;transition:.14s;white-space:nowrap}
.chip:hover{border-color:var(--em);color:var(--em)}
.chip.on{background:var(--em);border-color:var(--em);color:#f7f1e6}
html[data-theme="ink"] .chip.on{color:#15120c}
.chip .n{opacity:.6;margin-left:5px;font-family:var(--f-mono);font-size:11px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;vertical-align:middle}
.dot.text{background:var(--em)} .dot.image{background:var(--gold)}

/* prompt grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;align-items:start;padding-top:22px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;display:flex;flex-direction:column;gap:10px;transition:.16s}
.card:hover{border-color:var(--em)}
.card .meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.card .ct{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;color:var(--sienna);font-weight:600}
.signed{font-size:11px;color:var(--em);font-weight:600;display:inline-flex;align-items:center;gap:4px}
.card h3{font-family:var(--f-disp);font-weight:500;font-size:18px;line-height:1.25}
.card .yg{font-family:var(--f-serif);font-size:14.5px;color:var(--ink-2);line-height:1.45}
.card .yg b{color:var(--ink);font-weight:500;font-family:var(--f-ui);font-size:12.5px;letter-spacing:.3px}
.vars{display:flex;flex-wrap:wrap;gap:5px}
.var{font-family:var(--f-mono);font-size:11px;color:var(--gold);background:var(--em-soft);border:1px solid var(--line);padding:2px 7px;border-radius:2px}
.lvls{display:flex;gap:5px;flex-wrap:wrap}
.lv{font-size:11px;color:var(--ink-3);border:1px solid var(--line);padding:2px 8px;border-radius:2px}
.cbar{display:flex;gap:8px;margin-top:auto;padding-top:4px}
.copy{flex:1;font-family:var(--f-ui);font-weight:600;font-size:13.5px;padding:11px;border-radius:3px;cursor:pointer;border:1px solid var(--em);background:var(--em);color:#f7f1e6;transition:.16s;display:inline-flex;align-items:center;justify-content:center;gap:7px}
html[data-theme="ink"] .copy{color:#15120c}
.copy:hover{background:var(--em-ink)}
.copy.done{background:var(--gold);border-color:var(--gold);color:#2a1f08}
.view{font-family:var(--f-ui);font-weight:500;font-size:13px;padding:11px 15px;border-radius:3px;cursor:pointer;border:1px solid var(--line);background:transparent;color:var(--ink-2);transition:.16s}
.view:hover{border-color:var(--em);color:var(--em)}
.empty{text-align:center;color:var(--ink-3);padding:70px 0;font-family:var(--f-serif);font-size:18px}

/* tools */
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.tool{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;transition:.16s;display:block}
.tool:hover{border-color:var(--sienna)}
.tool h4{font-family:var(--f-disp);font-weight:500;font-size:18px;margin-bottom:5px;display:flex;align-items:center;gap:8px}
.tool h4 .a{color:var(--sienna);transition:.16s}
.tool:hover h4 .a{transform:translate(3px,-3px)}
.tool p{font-family:var(--f-serif);font-size:14px;color:var(--ink-3);line-height:1.45}

/* contact */
.contact{border:1px solid var(--line);border-radius:4px;padding:36px;text-align:center;background:var(--paper-2)}
.contact h2{font-family:var(--f-disp);font-weight:500;font-size:clamp(26px,4vw,38px);letter-spacing:-.6px;margin-bottom:8px}
.contact p{font-family:var(--f-serif);font-size:18px;color:var(--ink-2);max-width:540px;margin:0 auto 24px}
.icons{display:flex;gap:12px;justify-content:center;margin-bottom:22px}
.ico{width:52px;height:52px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;color:var(--ink-2);transition:.16s;background:var(--paper)}
.ico:hover{border-color:var(--em);color:var(--em);transform:translateY(-3px)}
.ico svg{width:22px;height:22px}
.fbk{display:inline-flex;align-items:center;gap:8px;font-family:var(--f-ui);font-weight:600;font-size:15px;padding:13px 26px;border-radius:3px;background:var(--em);color:#f7f1e6;border:1px solid var(--em);cursor:pointer}
html[data-theme="ink"] .fbk{color:#15120c}
.fbk:hover{background:var(--em-ink)}
.wsh{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:22px}
.wbtn{font-family:var(--f-ui);font-weight:600;font-size:13px;padding:9px 15px;border-radius:3px;cursor:pointer;border:1px solid var(--line);background:var(--paper);color:var(--ink-2);transition:.16s}
.wbtn:hover{border-color:var(--em);color:var(--em)}
.note{font-family:var(--f-serif);font-size:14px;color:var(--ink-3);margin-top:20px;font-style:italic}

footer{border-top:1px solid var(--line);padding:30px 0 46px;text-align:center;color:var(--ink-3);font-size:14px}
footer .h{font-family:var(--f-disp);font-style:italic;color:var(--ink-2);font-size:17px}
footer b{color:var(--ink-2)}

/* modal */
.modal{position:fixed;inset:0;z-index:90;display:none;align-items:center;justify-content:center;padding:20px;background:#0a0805aa;backdrop-filter:blur(4px)}
.modal.open{display:flex}
.sheet{width:min(720px,100%);max-height:88vh;overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:5px;padding:28px;position:relative}
.sheet .x{position:absolute;top:16px;right:16px;width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:transparent;color:var(--ink-2);cursor:pointer;font-size:16px}
.sheet h3{font-family:var(--f-disp);font-weight:500;font-size:25px;margin:8px 0 8px;letter-spacing:-.4px}
.sheet .yg{font-family:var(--f-serif);font-size:16px;color:var(--ink-2);margin-bottom:14px}
.lab{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin:14px 0 8px}
pre.full{white-space:pre-wrap;word-break:break-word;font-family:var(--f-mono);font-size:12.5px;line-height:1.6;color:var(--ink);
 background:var(--paper-2);border:1px solid var(--line);border-radius:3px;padding:16px;margin-bottom:14px}

#toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);opacity:0;z-index:100;
 background:var(--ink);color:var(--bg);padding:12px 20px;border-radius:3px;font-weight:600;font-size:14px;transition:.22s;pointer-events:none}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.reveal{opacity:0;transform:translateY(14px);animation:rise .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.reveal{animation:none;opacity:1;transform:none}*{scroll-behavior:auto!important}}
@media(max-width:560px){.grid{grid-template-columns:1fr}}
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
  <div class="sc eye reveal">Free · for teachers · ChatGPT · Claude · Gemini</div>
  <div class="hgrid">
    <div>
      <h1 class="title reveal" style="animation-delay:.05s"><span class="big">__COUNT__</span> prompts that<br>quietly do your<br><em>busywork.</em></h1>
      <div class="rule reveal" style="animation-delay:.1s"></div>
      <p class="lede reveal" style="animation-delay:.12s">Open one, fill the blanks, paste into any AI. Every answer comes <b>signed by you</b> — so students and parents can always find their teacher.</p>
      <div class="cta reveal" style="animation-delay:.18s"><a class="btn solid" href="#library">Browse the library</a><a class="btn line" href="#start">New to AI? Start here →</a></div>
    </div>
    <div class="aside reveal" style="animation-delay:.22s">
      <div class="num">__NCATS__</div><div class="nlab">Categories, neatly filed</div>
      <div class="mini"><div class="ct">Solutions</div><h4>Five handwritten methods, one problem</h4><p>Premium worked pages from a photo.</p></div>
      <div class="mini"><div class="ct">Practice · DPP</div><h4>30-question daily practice sheet</h4><p>With answer key &amp; difficulty bands.</p></div>
    </div>
  </div>
  <div class="stripe reveal" style="animation-delay:.26s"><span><b>100%</b> copy-paste</span><span><b>Auto-signed</b> answers</span><span><b>Free</b> forever</span><span><b>Works</b> offline</span></div>
</div></section>

<section id="start"><div class="wrap">
  <div class="shead"><div class="sc k">Start here · 60 seconds</div><h2>Never used AI? You'll be a pro in a minute.</h2></div>
  <div class="start">
    <div>
      <h3>Four small steps.</h3>
      <ol class="steps">
        <li><div><b>Open a free AI tool</b> — pick one on the right, no payment needed.</div></li>
        <li><div><b>Copy any prompt</b> from the library below (one tap).</div></li>
        <li><div><b>Paste &amp; fill the [BLANKS]</b> — e.g. [TOPIC] → Integration, [GRADE] → Class 12.</div></li>
        <li><div><b>Send.</b> To solve a photo of a question, attach the image, then paste the prompt.</div></li>
      </ol>
    </div>
    <div class="pick">
      <div class="lbl">Open a free AI tool</div>
      <div class="ai-row">
        <a class="ai" href="https://chatgpt.com" target="_blank" rel="noopener"><i></i>ChatGPT</a>
        <a class="ai" href="https://claude.ai" target="_blank" rel="noopener"><i></i>Claude</a>
        <a class="ai" href="https://gemini.google.com" target="_blank" rel="noopener"><i></i>Gemini</a>
      </div>
      <div class="ex"><div class="t">Try this first</div><div class="q">Act as a maths teacher. Solve this Class 10 question in 3
different methods, each on a clean page, with a one-line
"why this method" note. Question: [PASTE OR ATTACH IT]</div></div>
    </div>
  </div>
</div></section>

<section id="library"><div class="wrap">
  <div class="shead"><div class="sc k">The Library</div><h2>Browse every prompt</h2>
    <p>Tap a category to filter, or search. Each prompt is copy-paste ready and auto-signed.</p></div>
  <div class="cats" id="cats"></div>
</div></section>

<div class="controls"><div class="wrap">
  <div class="sb">
    <div class="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search prompts — DPP, integration, doubt, question paper, WhatsApp…" autocomplete="off"/>
    </div>
    <span class="shown" id="shown"></span>
  </div>
  <div class="frow" id="catChips"></div>
  <div class="frow">
    <span class="glab">Level</span><span id="lvlChips" style="display:contents"></span>
    <span class="glab" style="margin-left:10px">Type</span>
    <span class="chip tf on" data-type="all" onclick="setType('all',this)">All</span>
    <span class="chip tf" data-type="text" onclick="setType('text',this)"><span class="dot text"></span> Text</span>
    <span class="chip tf" data-type="image" onclick="setType('image',this)"><span class="dot image"></span> Image</span>
  </div>
</div></div>

<div class="wrap"><div class="grid" id="grid"></div></div>

<section id="tools"><div class="wrap">
  <div class="shead"><div class="sc k">More free tools</div><h2>Other projects by __AUTHOR__</h2>
    <p>More free, no-login resources for teachers and students.</p></div>
  <div class="tools" id="toolGrid"></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="contact">
    <div class="sc k" style="color:var(--sienna);margin-bottom:12px">Stay in touch</div>
    <h2>Feedback, problems or appreciation?</h2>
    <p>I'd love to hear how this helps your teaching — and what to add next. Tap to reach me.</p>
    <div class="icons" id="icons"></div>
    <div><a class="fbk" id="fbk"></a></div>
    <div class="wsh" id="wsh"></div>
    <p class="note">Every prompt signs each AI answer with my name and this site — so your students and parents can always find their teacher.</p>
  </div>
</div></section>

<footer><div class="wrap">
  <span class="h">Made for teachers, everywhere.</span><br><br>
  <b>__BRAND__</b> · __COUNT__ free prompts · Built __BUILD__ · Created &amp; curated by <b>__AUTHOR__</b> · __ROLE__<br>
  Free to share — please keep the credit.
</div></footer>

<div class="modal" id="modal"><div class="sheet" id="sheet"></div></div>
<div id="toast">Copied!</div>

<script id="DATA" type="application/json">__DATA__</script>
<script id="CFG" type="application/json">__CFG__</script>
<script>
const P=JSON.parse(document.getElementById('DATA').textContent);
const C=JSON.parse(document.getElementById('CFG').textContent);
const $=s=>document.querySelector(s);
const esc=s=>(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let st={q:'',cat:'all',level:'all',type:'all'};

const SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/></svg>';
const MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 109.8 9.8z"/></svg>';
const themeBtn=$('#theme');
function applyTheme(t){document.documentElement.dataset.theme=t;themeBtn.innerHTML=t==='day'?MOON:SUN;try{localStorage.setItem('ps-theme',t)}catch(e){}}
applyTheme((()=>{try{const v=localStorage.getItem('ps-theme');return (v==='day'||v==='ink')?v:'day'}catch(e){return 'day'}})());
themeBtn.onclick=()=>applyTheme(document.documentElement.dataset.theme==='day'?'ink':'day');

function copyText(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(()=>fb(t));}return Promise.resolve(fb(t));}
function fb(t){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.top='-9999px';document.body.appendChild(a);a.focus();a.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(a);}
let tT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(tT);tT=setTimeout(()=>t.classList.remove('show'),1500);}

const ICON={
 mail:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>',
 wa:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3a9 9 0 00-7.7 13.7L3 21l4.5-1.2A9 9 0 1012 3z"/><path d="M8.5 9.2c0 3 2.3 5.3 5.3 5.3 .5 0 1-.4 1-1l-.1-1-1.7-.6-.8.8c-.9-.4-1.6-1.1-2-2l.8-.8-.6-1.7-1-.1c-.6 0-1 .5-1 1z" fill="currentColor" stroke="none"/></svg>',
 ig:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>'
};
(function(){
 const c=C.contact;
 const links={mail:'mailto:'+c.email+'?subject='+encodeURIComponent('Feedback — '+C.brand),wa:'https://wa.me/'+c.wa_num,ig:'https://instagram.com/'+c.insta};
 const titles={mail:'Email me',wa:'WhatsApp me',ig:'Instagram'};
 const box=$('#icons');
 ['mail','wa','ig'].forEach(k=>{const a=document.createElement('a');a.className='ico';a.href=links[k];a.setAttribute('aria-label',titles[k]);a.title=titles[k];
   if(k!=='mail'){a.target='_blank';a.rel='noopener';}a.innerHTML=ICON[k];box.appendChild(a);});
 const f=$('#fbk');
 if(C.form){f.href=C.form;f.target='_blank';f.rel='noopener';}else{f.href=links.mail;}
 f.textContent='📝 Send feedback';
 const ws=$('#wsh');
 Object.keys(C.wa).forEach(k=>{const b=document.createElement('button');b.className='wbtn';b.textContent='Copy WhatsApp: '+k.replace(/ \(.*\)/,'');
   b.onclick=()=>{copyText(C.wa[k]);toast('WhatsApp message copied — paste into your group');};ws.appendChild(b);});
})();
(function(){const g=$('#toolGrid');C.tools.forEach(t=>{const a=document.createElement('a');a.className='tool';a.href=t.url;a.target='_blank';a.rel='noopener';
  a.innerHTML='<h4>'+esc(t.name)+' <span class="a">↗</span></h4><p>'+esc(t.desc)+'</p>';g.appendChild(a);});})();

const catCount=c=>P.filter(p=>p.category===c).length;
(function(){
 const cs=$('#cats');
 C.catOrder.forEach(c=>{const d=document.createElement('div');d.className='cat';
  const short=c.split(' & ')[0].split(', ')[0];
  d.innerHTML='<span class="n">'+catCount(c)+'</span><div class="ct">'+esc(short)+'</div><h4>'+esc(c)+'</h4><p>'+esc(C.catDesc[c]||'')+'</p>';
  d.onclick=()=>{setCat(c);document.querySelector('.controls').scrollIntoView({behavior:'smooth',block:'start'});};cs.appendChild(d);});
 const cc=$('#catChips');
 const all=document.createElement('span');all.className='chip on';all.dataset.cat='all';all.innerHTML='All <span class="n">'+P.length+'</span>';all.onclick=()=>setCat('all');cc.appendChild(all);
 C.catOrder.forEach(c=>{const s=document.createElement('span');s.className='chip';s.dataset.cat=c;s.innerHTML=esc(c)+' <span class="n">'+catCount(c)+'</span>';s.onclick=()=>setCat(c);cc.appendChild(s);});
 const lc=$('#lvlChips');
 const la=document.createElement('span');la.className='chip on';la.dataset.lvl='all';la.textContent='All';la.onclick=()=>setLevel('all');lc.appendChild(la);
 C.levels.forEach(l=>{const s=document.createElement('span');s.className='chip';s.dataset.lvl=l;s.textContent=l;s.onclick=()=>setLevel(l);lc.appendChild(s);});
})();
function setCat(c){st.cat=c;document.querySelectorAll('#catChips .chip').forEach(x=>x.classList.toggle('on',x.dataset.cat===c));render();}
function setLevel(l){st.level=l;document.querySelectorAll('#lvlChips .chip').forEach(x=>x.classList.toggle('on',x.dataset.lvl===l));render();}
function setType(t,el){st.type=t;document.querySelectorAll('.tf').forEach(x=>x.classList.toggle('on',x===el));render();}

function match(p){
 if(st.cat!=='all'&&p.category!==st.cat)return false;
 if(st.level!=='all'&&!(p.level||[]).includes(st.level))return false;
 if(st.type!=='all'&&p.output_type!==st.type)return false;
 if(st.q){const h=(p.title+' '+p.category+' '+(p.use_case||'')+' '+(p.what_you_get||'')+' '+p.prompt+' '+(p.variables||[]).join(' ')).toLowerCase();return st.q.split(/\s+/).every(w=>h.includes(w));}
 return true;
}
const grid=$('#grid');
function render(){
 const items=P.filter(match);
 $('#shown').textContent=items.length+' / '+P.length+' shown';
 grid.innerHTML='';
 if(!items.length){grid.innerHTML='<div class="empty">No prompts match. Try another word or category.</div>';return;}
 const fr=document.createDocumentFragment();
 items.forEach((p,i)=>{
  const card=document.createElement('article');card.className='card';
  const vars=(p.variables||[]).slice(0,6).map(v=>'<span class="var">'+esc(v)+'</span>').join('');
  const lvls=(p.level||[]).map(l=>'<span class="lv">'+esc(l)+'</span>').join('');
  const dot=p.output_type==='image'?'<span class="dot image" title="Makes an image"></span>':'<span class="dot text" title="Text answer"></span>';
  card.innerHTML='<div class="meta">'+dot+'<span class="ct">'+esc(p.category)+'</span><span class="signed">✍ signed</span></div>'+
   '<h3>'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg"><b>YOU GET — </b>'+esc(p.what_you_get)+'</p>':'')+
   (vars?'<div class="vars">'+vars+'</div>':'')+(lvls?'<div class="lvls">'+lvls+'</div>':'')+
   '<div class="cbar"><button class="copy">Copy prompt</button><button class="view">View</button></div>';
  const cp=card.querySelector('.copy');
  cp.onclick=()=>{copyText(p.prompt);cp.classList.add('done');cp.textContent='✓ Copied!';toast('Prompt copied — paste it into your AI');setTimeout(()=>{cp.classList.remove('done');cp.textContent='Copy prompt';},1600);};
  card.querySelector('.view').onclick=()=>openModal(p);
  if(i<9){card.classList.add('reveal');card.style.animationDelay=(i*0.03)+'s';}
  fr.appendChild(card);
 });
 grid.appendChild(fr);
}
const modal=$('#modal');
function openModal(p){
 const vars=(p.variables||[]).map(v=>'<span class="var">'+esc(v)+'</span>').join(' ');
 const lvls=(p.level||[]).map(l=>'<span class="lv">'+esc(l)+'</span>').join(' ');
 $('#sheet').innerHTML='<button class="x" onclick="closeModal()" aria-label="Close">✕</button>'+
  '<div class="meta"><span class="ct">'+esc(p.category)+'</span><span class="signed">✍ auto-signed</span></div>'+
  '<h3>'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg">'+esc(p.what_you_get)+'</p>':'')+
  (lvls?'<div class="lab">Best for</div><div class="lvls">'+lvls+'</div>':'')+
  (vars?'<div class="lab">Fill in these</div><div class="vars">'+vars+'</div>':'')+
  '<div class="lab">The prompt</div><pre class="full">'+esc(p.prompt)+'</pre>'+
  '<button class="copy" style="width:100%" id="mc">Copy this prompt</button>';
 $('#mc').onclick=()=>{copyText(p.prompt);toast('Prompt copied — paste it into your AI');const b=$('#mc');b.classList.add('done');b.textContent='✓ Copied!';setTimeout(()=>{b.classList.remove('done');b.textContent='Copy this prompt';},1600);};
 modal.classList.add('open');document.body.style.overflow='hidden';
}
function closeModal(){modal.classList.remove('open');document.body.style.overflow='';}
modal.onclick=e=>{if(e.target===modal)closeModal();};
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
let qt;$('#q').addEventListener('input',e=>{clearTimeout(qt);qt=setTimeout(()=>{st.q=e.target.value.trim().toLowerCase();render();},110);});
render();
</script>
</body>
</html>
"""

out=(TEMPLATE.replace("__BRAND__",esc(BRAND)).replace("__AUTHOR__",esc(AUTHOR)).replace("__ROLE__",esc(ROLE))
 .replace("__BUILD__",BUILD).replace("__COUNT__",str(COUNT)).replace("__NCATS__",str(len(used)))
 .replace("__DATA__",jsemb(prompts)).replace("__CFG__",jsemb(CONFIG)))
open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(out)

# prompt-pack.md
md=[f"# {BRAND}","",f"_{COUNT} copy-paste AI prompts for teachers — curated by {AUTHOR} ({ROLE}). Built {BUILD}._","",
 "Works with ChatGPT, Claude or Gemini. Open a prompt, replace the `[BRACKETS]`, paste it in. "
 "Every prompt signs its answer with a link back to this studio.",""]
by={}
for p in prompts: by.setdefault(p["category"],[]).append(p)
for c in used:
 md.append(f"\n## {c}  ({len(by[c])})\n")
 for p in by[c]:
  md.append(f"### {p['title']}")
  if p.get("what_you_get"): md.append(f"*You get: {p['what_you_get']}*")
  if p.get("variables"): md.append("Fill in: "+", ".join(f"`{v}`" for v in p["variables"]))
  md.append("\n```\n"+p["prompt"].strip()+"\n```\n")
open(os.path.join(HERE,"prompt-pack.md"),"w",encoding="utf-8").write("\n".join(md))

# WHATSAPP-MESSAGES.txt
wt=["="*60,f"  {BRAND} — WhatsApp messages (copy & paste)","="*60,""]
for k,v in WA.items(): wt+=[f"\n----- {k} -----\n",v,""]
wt+=["\nThe live link is in every message above:","  "+SITE_URL,
     "Contacts are click-only on the site (email / WhatsApp / Instagram) and are never shown as text."]
open(os.path.join(HERE,"WHATSAPP-MESSAGES.txt"),"w",encoding="utf-8").write("\n".join(wt))

print(f"Built index.html ({os.path.getsize(os.path.join(HERE,'index.html'))//1024} KB) · {COUNT} prompts · {len(used)} categories · {len(TOOLS)} tools")
