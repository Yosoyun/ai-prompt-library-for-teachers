#!/usr/bin/env python3
"""Build 'Prompt Studio' — Ivory Editorial, Teacher/Student, JEE/NEET/Olympiad/Foundation.
SEO-pre-rendered, accessible, performance-split (heavy prompt bodies lazy-loaded).
Run: python3 build_site.py
Outputs: index.html, bodies.json, prompt-pack.md, WHATSAPP-MESSAGES.txt, robots.txt, sitemap.xml, og-cover.svg
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
      "prompt":(p.get("prompt") or "").strip(),"tool":(p.get("tool") or "Any").strip(),
      "added":p.get("added",""),"popular":bool(p.get("popular")),"sample":(p.get("sample") or "").strip()})
COUNT=len(prompts)

# light index (no heavy body) + separate bodies map
_IK=("id","mode","track","subject","category","title","use_case","what_you_get","level","output_type","interactive","variables")
INDEX=[dict({k:p[k] for k in _IK}, added=p.get("added",""), popular=bool(p.get("popular")), sample=p.get("sample","")) for p in prompts]
BODIES={p["id"]:p["prompt"] for p in prompts}

def esc(s): return html.escape(s or "",quote=True)
def jsemb(o): return json.dumps(o,ensure_ascii=False).replace("</","<\\/")

WA={
"Invite (English)":"🎓 *"+BRAND+" — for teachers & students*\n\n"+str(COUNT)+"+ premium, copy-paste AI prompts for JEE, NEET, Olympiad & school — solutions, mock papers, doubt-solving, study plans, lesson plans and more. Many ask you a few questions first, then give a premium answer. Attach a photo of any question and they solve it.\n\n✅ Works on ChatGPT, Claude or Gemini (free too).\n🧩 Pick Teacher or Student → choose a prompt → fill the [BLANKS] → paste.\n\n👉 "+SITE_URL+"\n\nMade for teachers & students, by "+AUTHOR+".",
"How to use it daily (English)":"📌 *How to use "+BRAND+" every day*\n\n1️⃣ Open the link, bookmark it.\n2️⃣ Tap *Teacher* or *Student* mode.\n3️⃣ Pick your track — JEE / NEET / Olympiad / Foundation — and subject.\n4️⃣ Tap *Copy* or *Open ↗*, paste into ChatGPT / Claude / Gemini.\n5️⃣ Answer its questions (many ask first), or attach your question's photo.\n6️⃣ Get a premium, exam-accurate answer.\n\n👉 "+SITE_URL,
"Invite (Hindi)":"🎓 *"+BRAND+" — शिक्षकों और छात्रों के लिए*\n\n"+str(COUNT)+"+ प्रीमियम, कॉपी-पेस्ट AI प्रॉम्प्ट — JEE, NEET, Olympiad और स्कूल के लिए। हल, मॉक पेपर, डाउट सॉल्विंग, स्टडी प्लान और बहुत कुछ। कई प्रॉम्प्ट पहले आपसे सवाल पूछते हैं, फिर प्रीमियम उत्तर देते हैं।\n\n✅ ChatGPT, Claude या Gemini पर चलता है।\n👉 "+SITE_URL+"\n\n— "+AUTHOR,
}

CONFIG={"brand":BRAND,"author":AUTHOR,"role":ROLE,"site":SITE_URL,"count":COUNT,
 "contact":CONTACT,"form":FEEDBACK_FORM_URL,"tools":TOOLS,"modes":MODES,
 "trackOrder":TRACK_ORDER,"trackLabel":TRACK_LABEL,"levels":LEVELS,"wa":WA}

# ---- pre-rendered static cards (SEO / no-JS) ----
def static_card(p):
    badges=""
    if p["interactive"]: badges+='<span class="badge ask">asks first</span>'
    if p["output_type"]=="image": badges+='<span class="badge pic">photo</span>'
    return (f'<article class="card"><div class="meta"><span class="ct">{esc(p["track"])} · {esc(p["subject"])}</span></div>'
            f'<div class="tagrow">{badges}</div><h3>{esc(p["title"])}</h3>'
            f'<p class="yg"><b>YOU GET — </b>{esc(p["what_you_get"])}</p>'
            f'<div class="meta"><span class="ct" style="color:var(--ink-3)">{esc(p["category"])}</span></div></article>')
STATIC_CARDS="".join(static_card(p) for p in prompts)

# ---- JSON-LD ----
JSONLD={"@context":"https://schema.org","@graph":[
 {"@type":"WebSite","@id":SITE_URL+"#website","url":SITE_URL,"name":BRAND+" — AI Prompts for Teachers & Students",
  "description":f"{COUNT}+ premium copy-paste AI prompts for JEE, NEET, Olympiad and school.",
  "inLanguage":"en","potentialAction":{"@type":"SearchAction","target":SITE_URL+"?q={search_term_string}","query-input":"required name=search_term_string"}},
 {"@type":"Person","@id":SITE_URL+"#author","name":AUTHOR,"jobTitle":ROLE,"url":SITE_URL,
  "sameAs":["https://instagram.com/"+CONTACT["insta"]]},
 {"@type":"CollectionPage","@id":SITE_URL,"url":SITE_URL,"name":BRAND,"isPartOf":{"@id":SITE_URL+"#website"},
  "about":["JEE preparation","NEET preparation","Mathematical Olympiad","AI prompts for teachers","AI prompts for students"],
  "creator":{"@id":SITE_URL+"#author"}},
 {"@type":"ItemList","name":"AI prompt categories","numberOfItems":COUNT,
  "itemListElement":[{"@type":"ListItem","position":i+1,"name":t} for i,t in enumerate(sorted({p["category"] for p in prompts}))]},
 {"@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":"Is Prompt Studio free?","acceptedAnswer":{"@type":"Answer","text":"Yes — all "+str(COUNT)+"+ prompts are free to copy and use, with no login."}},
   {"@type":"Question","name":"Which AI tools do these prompts work with?","acceptedAnswer":{"@type":"Answer","text":"Any modern AI assistant — ChatGPT, Claude or Gemini, including their free versions."}},
   {"@type":"Question","name":"Do the prompts cover JEE, NEET and Olympiad?","acceptedAnswer":{"@type":"Answer","text":"Yes. Prompts are organised by Teacher and Student mode across JEE, NEET, Olympiad and Foundation/Boards tracks, in Physics, Chemistry, Biology and Maths."}},
   {"@type":"Question","name":"Can I solve a question from a photo?","acceptedAnswer":{"@type":"Answer","text":"Yes — many prompts are photo-aware: attach a picture of the question and the AI transcribes then solves it step by step."}}]}
]}

TITLE="AI Prompts for Teachers & Students — JEE, NEET & Olympiad | "+BRAND
DESC=f"{COUNT}+ free, premium copy-paste AI prompts for teachers and students — JEE, NEET, Olympiad and school. Interview-first and photo-aware. Works with ChatGPT, Claude and Gemini."
FAVICON="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231c4a3a'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-style='italic' font-size='20' fill='%23f7f1e6' text-anchor='middle'%3EP%3C/text%3E%3C/svg%3E"

TEMPLATE=r"""<!DOCTYPE html>
<html lang="en" data-theme="day">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>__TITLE__</title>
<meta name="description" content="__DESC__"/>
<link rel="canonical" href="__SITE__"/>
<meta name="theme-color" content="#f7f1e6"/>
<meta name="author" content="__AUTHOR__"/>
<link rel="icon" href="__FAVICON__"/>
<link rel="apple-touch-icon" href="og-cover.png"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="__BRAND__"/>
<meta property="og:title" content="__TITLE__"/>
<meta property="og:description" content="__DESC__"/>
<meta property="og:url" content="__SITE__"/>
<meta property="og:image" content="__SITE__og-cover.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="__TITLE__"/>
<meta name="twitter:description" content="__DESC__"/>
<meta name="twitter:image" content="__SITE__og-cover.png"/>
<script type="application/ld+json">__JSONLD__</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Hanken+Grotesk:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#f7f1e6;--paper:#fffdf7;--paper-2:#fbf6ec;--ink:#211d16;--ink-2:#463f33;--ink-3:#5a5347;
 --line:#211d1626;--line-2:#211d1612;--em:#1c4a3a;--em-ink:#123528;--em-soft:#1c4a3a14;--sienna:#8f4426;--gold:#946615;--blue:#2f5d86;
 --f-disp:"Fraunces",Georgia,serif;--f-serif:"Newsreader",Georgia,serif;--f-ui:"Hanken Grotesk",-apple-system,sans-serif;--f-mono:"JetBrains Mono",ui-monospace,monospace;--maxw:1140px;}
html[data-theme="ink"]{--bg:#15120c;--paper:#1e1a12;--paper-2:#241f15;--ink:#ece3d2;--ink-2:#c0b6a0;--ink-3:#9a907d;
 --line:#ffffff24;--line-2:#ffffff12;--em:#7cc6a3;--em-ink:#bfe7d4;--em-soft:#7cc6a31a;--sienna:#e09a6c;--gold:#e2b667;--blue:#8fb8de;}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--f-ui);font-size:16px;line-height:1.55;
 background-image:radial-gradient(var(--line-2) 1px,transparent 1px);background-size:22px 22px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}::selection{background:var(--em);color:var(--bg)}
:focus-visible{outline:2.5px solid var(--em);outline-offset:2px;border-radius:3px}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 40px}
@media(max-width:640px){.wrap{padding:0 20px}}
.skip{position:absolute;left:-9999px;top:8px;z-index:200;background:var(--em);color:#f7f1e6;padding:10px 16px;border-radius:4px;font-weight:600}
.skip:focus{left:12px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.sc{font-family:var(--f-ui);font-size:12px;font-weight:600;letter-spacing:2.4px;text-transform:uppercase}
header.nav{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
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
.modebar{display:flex;justify-content:center;margin-bottom:14px}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:4px;background:var(--paper);padding:4px;gap:4px}
.seg button{font-family:var(--f-ui);font-weight:600;font-size:15px;padding:10px 26px;border:none;border-radius:3px;background:transparent;color:var(--ink-2);cursor:pointer;transition:.16s;display:inline-flex;align-items:center;gap:8px}
.seg button[aria-pressed="true"]{background:var(--em);color:#f7f1e6}
html[data-theme="ink"] .seg button[aria-pressed="true"]{color:#15120c}
.controls{position:sticky;top:66px;z-index:40;background:var(--bg);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0}
.sb{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;font-family:var(--f-ui);font-size:15px;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:12px 14px 12px 42px;outline:none;transition:.16s}
.search input::placeholder{color:var(--ink-3)}.search input:focus{border-color:var(--em)}
.search svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);stroke:var(--ink-3)}
.shown{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.clr{font-family:var(--f-ui);font-weight:600;font-size:12.5px;padding:7px 12px;border:1px solid var(--line);border-radius:3px;background:transparent;color:var(--sienna);cursor:pointer;display:none}
.clr.show{display:inline-block}
.frow{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:10px}
.glab{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin-right:3px}
.chip{font-family:var(--f-ui);font-size:13px;font-weight:500;padding:7px 12px;border:1px solid var(--line);border-radius:3px;background:var(--paper);color:var(--ink-2);cursor:pointer;transition:.14s;white-space:nowrap}
.chip:hover{border-color:var(--em);color:var(--em)}.chip[aria-pressed="true"]{background:var(--em);border-color:var(--em);color:#f7f1e6}
html[data-theme="ink"] .chip[aria-pressed="true"]{color:#15120c}
.chip .n{opacity:.6;margin-left:5px;font-family:var(--f-mono);font-size:11px}
.openhint{font-family:var(--f-serif);font-size:13px;color:var(--ink-3);margin-top:8px;font-style:italic}
.filt-toggle{font-family:var(--f-ui);font-weight:600;font-size:13px;padding:8px 13px;border:1px solid var(--line);border-radius:3px;background:var(--paper);color:var(--ink-2);cursor:pointer;display:none}
.filt-toggle:hover{border-color:var(--em);color:var(--em)}
.facets{display:block}
.controls.collapsed .facets{display:none}
.chip[disabled]{opacity:.34;cursor:not-allowed;pointer-events:none}
.badge.new{color:#fff;background:var(--sienna);border-color:var(--sienna)}
.card h3,.card .ct,.var,.tool h4{overflow-wrap:anywhere}
#shareBtn{cursor:pointer}
.hint{font-family:var(--f-serif);font-size:13.5px;color:var(--ink-3);margin:2px 0 10px;font-style:italic;line-height:1.45}
.badge.pop{color:var(--gold);border-color:color-mix(in srgb,var(--gold) 50%,transparent);font-weight:700}
details.sample{margin:4px 0 14px;border:1px solid var(--line);border-radius:3px;background:var(--paper-2)}
details.sample summary{cursor:pointer;padding:11px 14px;font-weight:600;font-size:13.5px;color:var(--em);list-style:none}
details.sample summary::-webkit-details-marker{display:none}
details.sample pre.full{margin:0 14px 14px;background:var(--paper)}
.n[id]{font-family:var(--f-mono);font-size:11px;opacity:.7}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;vertical-align:middle}.dot.text{background:var(--em)}.dot.image{background:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(322px,1fr));gap:14px;align-items:start;padding-top:22px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:18px;display:flex;flex-direction:column;gap:10px;transition:border-color .16s,transform .16s;content-visibility:auto;contain-intrinsic-size:auto 300px}
.card:hover{border-color:var(--em)}
.card .meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.card .ct{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;color:var(--sienna);font-weight:600}
.card h3{font-family:var(--f-disp);font-weight:500;font-size:18px;line-height:1.25}
.card .yg{font-family:var(--f-serif);font-size:14.5px;color:var(--ink-2);line-height:1.45}
.card .yg b{color:var(--ink);font-weight:600;font-family:var(--f-ui);font-size:12px;letter-spacing:.3px}
.tagrow{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.badge{font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:2px;border:1px solid var(--line);color:var(--ink-3);letter-spacing:.3px}
.badge.ask{color:var(--blue);border-color:color-mix(in srgb,var(--blue) 40%,transparent)}
.badge.pic{color:var(--gold);border-color:color-mix(in srgb,var(--gold) 45%,transparent)}
.star{margin-left:auto;background:none;border:none;cursor:pointer;font-size:17px;line-height:1;color:var(--ink-3);padding:2px;transition:.15s}
.star:hover{color:var(--gold);transform:scale(1.15)}.star[aria-pressed="true"]{color:var(--gold)}
.vars{display:flex;flex-wrap:wrap;gap:5px}
.var{font-family:var(--f-mono);font-size:11px;color:var(--gold);background:var(--em-soft);border:1px solid var(--line);padding:2px 7px;border-radius:2px}
.cbar{display:flex;gap:8px;margin-top:auto;padding-top:4px;flex-wrap:wrap}
.copy{flex:1;min-width:90px;font-family:var(--f-ui);font-weight:600;font-size:13.5px;padding:11px;border-radius:3px;cursor:pointer;border:1px solid var(--em);background:var(--em);color:#f7f1e6;transition:.16s}
html[data-theme="ink"] .copy{color:#15120c}.copy:hover{background:var(--em-ink)}.copy.done{background:var(--gold);border-color:var(--gold);color:#2a1f08}
.open,.view{font-family:var(--f-ui);font-weight:600;font-size:13px;padding:11px 14px;border-radius:3px;cursor:pointer;border:1px solid var(--em);background:transparent;color:var(--em);transition:.16s}
.view{border-color:var(--line);color:var(--ink-2);font-weight:500}
.open:hover{background:var(--em-soft)}.view:hover{border-color:var(--em);color:var(--em)}
.more{display:flex;justify-content:center;padding:30px 0 8px}
.empty{text-align:center;color:var(--ink-2);padding:54px 0;font-family:var(--f-serif)}
.empty .sum{font-size:14px;color:var(--ink-3);margin:8px 0 16px;font-family:var(--f-ui)}
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
.modal{position:fixed;inset:0;z-index:90;display:none;align-items:center;justify-content:center;padding:20px;background:#0a0805bb;backdrop-filter:blur(4px)}
.modal.open{display:flex}
.sheet{width:min(720px,100%);max-height:88vh;overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:5px;padding:28px;position:relative}
.sheet .x{position:absolute;top:16px;right:16px;width:38px;height:38px;border:1px solid var(--line);border-radius:50%;background:transparent;color:var(--ink-2);cursor:pointer;font-size:16px}
.sheet h3{font-family:var(--f-disp);font-weight:500;font-size:25px;margin:8px 0 8px;letter-spacing:-.4px}
.sheet .yg{font-family:var(--f-serif);font-size:16px;color:var(--ink-2);margin-bottom:14px}
.lab{font-size:11px;letter-spacing:1.1px;text-transform:uppercase;color:var(--ink-3);font-weight:600;margin:14px 0 8px}
pre.full{white-space:pre-wrap;word-break:break-word;font-family:var(--f-mono);font-size:13px;line-height:1.6;color:var(--ink);background:var(--paper-2);border:1px solid var(--line);border-radius:3px;padding:16px;margin-bottom:14px}
#toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);opacity:0;z-index:100;background:var(--ink);color:var(--bg);padding:12px 20px;border-radius:3px;font-weight:600;font-size:14px;transition:.22s;pointer-events:none}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.reveal{opacity:0;transform:translateY(14px);animation:rise .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.reveal{animation:none;opacity:1;transform:none}*{scroll-behavior:auto!important;transition-duration:.001ms!important;animation-duration:.001ms!important}.card:hover,.star:hover,.btn:hover{transform:none}}
@media(max-width:760px){
 header.nav{backdrop-filter:none}.controls{position:static}
 .filt-toggle{display:inline-block}
 .frow{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px;scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 90%,transparent);mask-image:linear-gradient(90deg,#000 90%,transparent)}
 .frow::-webkit-scrollbar{display:none}
 .frow .glab{position:sticky;left:0;background:var(--bg);padding-right:8px;z-index:2}
 .chip,.seg button{flex:0 0 auto}
 .chip,.clr,.filt-toggle,.tf,.star{min-height:42px}.star{min-width:42px}
 .sheet{padding:20px}.sheet .cbar{flex-direction:column}.sheet .cbar .open,.sheet .cbar .copy{width:100%}
}
@media(max-width:560px){.grid{grid-template-columns:1fr}.seg button{padding:10px 18px}}
</style>
</head>
<body>
<a class="skip" href="#grid">Skip to prompts</a>
<a id="top"></a>
<header class="nav"><div class="wrap row">
  <a class="brand" href="#top"><span class="seal" aria-hidden="true">P</span>__BRAND__</a>
  <nav aria-label="Primary"><a href="#start" data-i18n="nav.start">Start here</a><a href="#library" data-i18n="nav.lib">Library</a><a href="#tools" data-i18n="nav.tools">Tools</a><a href="#contact" data-i18n="nav.contact">Contact</a></nav>
  <button class="tg" id="lang" aria-label="Switch language English / Hindi" title="English / हिन्दी" style="font-family:var(--f-ui);font-weight:700;font-size:13px">हिं</button>
  <button class="tg" id="theme" aria-label="Toggle day or ink mode" title="Day / Ink"></button>
</div></header>

<section class="hero"><div class="wrap">
  <div class="sc eye reveal" data-i18n="hero.eye">Free · teachers &amp; students · JEE · NEET · Olympiad · Boards</div>
  <h1 class="title reveal" style="animation-delay:.05s" data-i18n="hero.h1"><span class="big">__COUNT__+</span> premium prompts that<br>think <em>with</em> you, not for you.</h1>
  <p class="lede reveal" style="animation-delay:.12s" data-i18n="hero.lede">Master prompts for every teacher and student. Many <b>ask you a few questions first</b>, then deliver a premium, exam-accurate answer. <b>Attach a photo</b> of any question and they solve it — step by step.</p>
  <div class="cta reveal" style="animation-delay:.18s"><a class="btn solid" href="#library" data-i18n="hero.cta1">Open the library</a><a class="btn line" href="#start" data-i18n="hero.cta2">New to AI? Start here →</a><button class="btn line" id="shareBtn" data-i18n="hero.share">↗ Share with a teacher</button></div>
  <div class="stripe reveal" style="animation-delay:.24s"><span><b>__COUNT__+</b> <span data-i18n="stat.prompts">prompts</span></span><span><b>2</b> <span data-i18n="stat.modes">modes</span></span><span><b>4</b> <span data-i18n="stat.tracks">tracks</span></span><span><b>Photo</b><span data-i18n="stat.photo">-aware</span></span><span><b>Free</b> <span data-i18n="stat.free">forever</span></span></div>
</div></section>

<section id="start"><div class="wrap">
  <div class="shead"><div class="sc k" data-i18n="start.k">Start here · 60 seconds</div><h2 data-i18n="start.h2">Two modes. Pick yours.</h2>
    <p data-i18n="start.sub">👩‍🏫 <b>Teacher</b> — solutions, mock papers, lessons, doubt-clinics. 🎓 <b>Student</b> — a tutor, photo doubt-solving, prep plans.</p></div>
  <div class="start">
    <div><h3>Four small steps.</h3>
      <ol class="steps">
        <li><div><b>Open a free AI tool</b> — pick one on the right.</div></li>
        <li><div><b>Choose Teacher or Student</b>, then your track &amp; subject.</div></li>
        <li><div><b>Copy or Open ↗ a prompt</b>; answer its questions or attach your question's photo.</div></li>
        <li><div><b>Get a premium answer</b> you can use straight away.</div></li>
      </ol>
    </div>
    <div class="pick"><div class="lbl">Open a free AI tool</div>
      <div class="ai-row">
        <a class="ai" href="https://chatgpt.com" target="_blank" rel="noopener"><i aria-hidden="true"></i>ChatGPT</a>
        <a class="ai" href="https://claude.ai" target="_blank" rel="noopener"><i aria-hidden="true"></i>Claude</a>
        <a class="ai" href="https://gemini.google.com" target="_blank" rel="noopener"><i aria-hidden="true"></i>Gemini</a>
      </div>
      <div class="ex"><div class="t">What "asks-first" feels like</div><div class="q">You: *copy a tutor prompt*
AI: "Before I solve — what's your class &amp; target exam,
and where exactly are you stuck? (1/4)"
You: answer · AI guides you to the answer.</div></div>
      <p class="hint">📎 To solve from a photo: in the AI, tap the <b>paperclip / +</b> icon, choose your question's photo, then paste the prompt and send.</p>
    </div>
  </div>
</div></section>

<section id="library"><div class="wrap">
  <div class="shead"><div class="sc k" data-i18n="lib.k">The Library</div><h2 data-i18n="lib.h2">__COUNT__+ premium prompts</h2>
    <p>Switch modes, choose a track &amp; subject, or search. Look for the <span style="color:var(--blue);font-weight:600">asks first</span> and <span style="color:var(--gold);font-weight:600">photo</span> badges, and ★ your favourites.</p></div>
  <div class="modebar"><div class="seg" id="modeSeg" role="group" aria-label="Mode"></div></div>
</div></section>

<div class="controls"><div class="wrap">
  <div class="sb">
    <div class="search"><label for="q" class="sr">Search prompts</label>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search prompts — mock test, doubt, study plan, integration, NCERT…" autocomplete="off"/></div>
    <button class="filt-toggle" id="filtToggle" aria-expanded="true">⚙ Filters</button>
    <span class="shown" id="shown" aria-live="polite"></span>
    <button class="clr" id="clr">✕ Clear</button>
  </div>
  <div class="facets" id="facets">
  <div class="frow"><span class="glab" data-i18n="f.track">Track</span><span id="trackChips" style="display:contents"></span></div>
  <div class="frow"><span class="glab" data-i18n="f.subject">Subject</span><span id="subChips" style="display:contents"></span></div>
  <div class="frow"><span class="glab" title="What you want the AI to do" data-i18n="f.iwant">I want</span><span id="catChips" style="display:contents"></span></div>
  <div class="frow"><span class="glab" data-i18n="f.output">Output</span>
    <button class="chip tf" data-type="all" aria-pressed="true" onclick="setType('all',this)">All</button>
    <button class="chip tf" data-type="text" aria-pressed="false" onclick="setType('text',this)"><span class="dot text"></span> Text <span class="n" id="cText"></span></button>
    <button class="chip tf" data-type="image" aria-pressed="false" onclick="setType('image',this)"><span class="dot image"></span> Photo <span class="n" id="cImg"></span></button>
    <button class="chip" id="askChip" aria-pressed="false" onclick="toggleAsk(this)">💬 Asks first <span class="n" id="cAsk"></span></button>
    <button class="chip" id="popChip" aria-pressed="false" onclick="togglePop(this)">🔥 Popular <span class="n" id="cPop"></span></button>
    <button class="chip" id="favChip" aria-pressed="false" onclick="toggleFav(this)">★ Saved <span class="n" id="cSaved"></span></button>
  </div>
  <div class="frow"><span class="glab" title="Which AI the Open button launches" data-i18n="f.open">When I tap Open</span><span id="aiChips" style="display:contents"></span></div>
  </div>
  <p class="openhint">Tip: anything in <b>[SQUARE BRACKETS]</b> is a blank — fill it in or delete it. <b>Open ↗</b> copies the prompt and opens your AI; just paste (Ctrl/Cmd+V) if it isn't pre-filled.</p>
</div></div>

<div class="wrap"><div class="grid" id="grid">__STATIC__</div><div class="more" id="more"></div></div>

<section id="tools"><div class="wrap">
  <div class="shead"><div class="sc k">More free tools</div><h2>Other projects by __AUTHOR__</h2><p>More free, no-login resources for teachers and students.</p></div>
  <div class="tools" id="toolGrid"></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="contact">
    <div class="sc k" style="color:var(--sienna);margin-bottom:12px">Stay in touch</div>
    <h2 data-i18n="contact.h2">Feedback, problems or appreciation?</h2>
    <p>I'd love to hear how this helps — and what to add next. Tap to reach me.</p>
    <div class="icons" id="icons"></div>
    <div><a class="fbk" id="fbk"></a></div>
    <div class="wsh" id="wsh"></div>
    <p class="note">Every prompt signs each AI answer with my name and this site — so students and parents can always find their teacher.</p>
  </div>
</div></section>

<footer><div class="wrap"><span class="h">Made for teachers &amp; students, everywhere.</span><br><br>
  <b>__BRAND__</b> · __COUNT__+ premium prompts · Built __BUILD__ · Created &amp; curated by <b>__AUTHOR__</b> · __ROLE__<br>Free to share — please keep the credit.</div></footer>

<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="sheetTitle"><div class="sheet" id="sheet"></div></div>
<div id="toast" role="status" aria-live="polite">Copied!</div>

<script id="DATA" type="application/json">__DATA__</script>
<script id="CFG" type="application/json">__CFG__</script>
<script>
"use strict";
var P,C;
try{ P=JSON.parse(document.getElementById('DATA').textContent); C=JSON.parse(document.getElementById('CFG').textContent); }
catch(e){ document.getElementById('grid').innerHTML='<div class="empty">Sorry — the prompt list failed to load. Please refresh the page.</div>'; }
if(P&&C){(function(){
const $=s=>document.querySelector(s);
const esc=s=>(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const PAGE=48;
const ls=(k,d)=>{try{return JSON.parse(localStorage.getItem(k))||d}catch(e){return d}};
const lset=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
let favs=new Set(ls('ps-fav',[]));
let st={mode:'Teacher',track:'all',sub:'all',cat:'all',type:'all',ask:false,fav:false,pop:false,q:'',shown:PAGE,ai:(ls('ps-ai','chatgpt'))};

/* lazy bodies */
let BODIES={},bodiesP=null;
function loadBodies(){ if(!bodiesP) bodiesP=fetch('bodies.json').then(r=>r.json()).then(b=>{BODIES=b;return b}).catch(()=>({})); return bodiesP; }
if(window.requestIdleCallback){requestIdleCallback(()=>loadBodies(),{timeout:2000});}else{setTimeout(()=>loadBodies(),1200);}
async function getBody(id){ if(BODIES[id])return BODIES[id]; const b=await loadBodies(); return b[id]||'(Prompt text could not load — please refresh.)'; }

/* theme */
const SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/></svg>';
const MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 109.8 9.8z"/></svg>';
const tb=$('#theme');
function applyTheme(t){document.documentElement.dataset.theme=t;tb.innerHTML=t==='day'?MOON:SUN;try{localStorage.setItem('ps-theme',t)}catch(e){}}
applyTheme((()=>{try{const v=localStorage.getItem('ps-theme');return (v==='day'||v==='ink')?v:'day'}catch(e){return 'day'}})());
tb.onclick=()=>applyTheme(document.documentElement.dataset.theme==='day'?'ink':'day');
/* language (Hindi UI for the chrome) */
const I18N_HI={
 'nav.start':'शुरू करें','nav.lib':'लाइब्रेरी','nav.tools':'टूल्स','nav.contact':'संपर्क',
 'hero.eye':'मुफ़्त · शिक्षक और छात्र · JEE · NEET · ओलंपियाड · बोर्ड्स',
 'hero.h1':'<span class="big">'+C.count+'+</span> प्रीमियम प्रॉम्प्ट जो<br>आपके <em>साथ</em> सोचते हैं, आपके बदले नहीं।',
 'hero.lede':'हर शिक्षक और छात्र के लिए मास्टर प्रॉम्प्ट। कई पहले <b>आपसे कुछ सवाल पूछते हैं</b>, फिर परीक्षा-सटीक, प्रीमियम उत्तर देते हैं। किसी भी सवाल की <b>फोटो लगाइए</b> — वे कदम-दर-कदम हल कर देते हैं।',
 'hero.cta1':'लाइब्रेरी खोलें','hero.cta2':'AI में नए हैं? यहाँ से शुरू करें →','hero.share':'↗ किसी शिक्षक के साथ शेयर करें',
 'stat.prompts':'प्रॉम्प्ट','stat.modes':'मोड','stat.tracks':'ट्रैक','stat.photo':' — फोटो सक्षम','stat.free':'हमेशा',
 'start.k':'यहाँ से शुरू करें · 60 सेकंड','start.h2':'दो मोड। अपना चुनें।',
 'start.sub':'👩‍🏫 <b>शिक्षक</b> — हल, मॉक पेपर, लेसन, डाउट-क्लिनिक। 🎓 <b>छात्र</b> — ट्यूटर, फोटो डाउट-सॉल्विंग, तैयारी प्लान।',
 'f.track':'ट्रैक','f.subject':'विषय','f.iwant':'मुझे चाहिए','f.output':'आउटपुट','f.open':'Open दबाने पर',
 'lib.k':'लाइब्रेरी','lib.h2':C.count+'+ प्रीमियम प्रॉम्प्ट','contact.h2':'फीडबैक, समस्या या सराहना?'
};
const i18nEN={};
function applyLang(l){document.documentElement.lang=(l==='hi'?'hi':'en');
 document.querySelectorAll('[data-i18n]').forEach(el=>{const k=el.getAttribute('data-i18n');if(!(k in i18nEN))i18nEN[k]=el.innerHTML;el.innerHTML=(l==='hi'&&I18N_HI[k])?I18N_HI[k]:i18nEN[k];});
 const lb=document.getElementById('lang');if(lb)lb.textContent=(l==='hi'?'EN':'हिं');try{localStorage.setItem('ps-lang',l)}catch(e){}}
(function(){const lb=document.getElementById('lang');if(lb)lb.onclick=()=>applyLang(document.documentElement.lang==='hi'?'en':'hi');
 applyLang((()=>{try{return localStorage.getItem('ps-lang')==='hi'?'hi':'en'}catch(e){return 'en'}})());})();

function copyText(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(()=>fbcopy(t));}return Promise.resolve(fbcopy(t));}
function fbcopy(t){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.top='-9999px';document.body.appendChild(a);a.focus();a.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(a);}
let tT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(tT);tT=setTimeout(()=>t.classList.remove('show'),1600);}

const AINAME={chatgpt:'ChatGPT',claude:'Claude',gemini:'Gemini'};
function buildAI(){const box=$('#aiChips');box.innerHTML='';['chatgpt','claude','gemini'].forEach(a=>{const b=document.createElement('button');b.className='chip';b.setAttribute('aria-pressed',st.ai===a);b.textContent=AINAME[a];b.onclick=()=>{st.ai=a;lset('ps-ai',a);buildAI();render();};box.appendChild(b);});}
const BARE={chatgpt:'https://chatgpt.com/',claude:'https://claude.ai/new',gemini:'https://gemini.google.com/app'};
function openAI(id){const ai=st.ai||'chatgpt';pushRecent(id);
 if(BODIES[id]){const text=BODIES[id];copyText(text);const enc=encodeURIComponent(text);const url=(ai==='chatgpt'&&enc.length<5000)?'https://chatgpt.com/?q='+enc:BARE[ai];window.open(url,'_blank','noopener');toast('Copied — opening '+AINAME[ai]+'. Paste with Ctrl/Cmd+V.');}
 else{window.open(BARE[ai],'_blank','noopener');toast('Opening '+AINAME[ai]+' — copying the prompt, paste it in a moment.');getBody(id).then(b=>{if(b&&b.indexOf('could not load')===-1)copyText(b);});}}
function pushRecent(id){let r=ls('ps-recent',[]);r=[id].concat(r.filter(x=>x!==id)).slice(0,30);lset('ps-recent',r);}

(function(){const c=C.contact;const links={mail:'mailto:'+c.email+'?subject='+encodeURIComponent('Feedback — '+C.brand),wa:'https://wa.me/'+c.wa_num,ig:'https://instagram.com/'+c.insta};
 const ICON={mail:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/></svg>',
  wa:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 3a9 9 0 00-7.7 13.7L3 21l4.5-1.2A9 9 0 1012 3z"/></svg>',
  ig:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>'};
 const titles={mail:'Email me',wa:'WhatsApp me',ig:'Instagram'};const box=$('#icons');
 ['mail','wa','ig'].forEach(k=>{const a=document.createElement('a');a.className='ico';a.href=links[k];a.setAttribute('aria-label',titles[k]);a.title=titles[k];if(k!=='mail'){a.target='_blank';a.rel='noopener';}a.innerHTML=ICON[k];box.appendChild(a);});
 const f=$('#fbk');if(C.form){f.href=C.form;f.target='_blank';f.rel='noopener';}else{f.href=links.mail;}f.textContent='📝 Send feedback';
 const ws=$('#wsh');Object.keys(C.wa).forEach(k=>{const b=document.createElement('button');b.className='wbtn';b.textContent='Copy WhatsApp: '+k.replace(/ \(.*\)/,'');b.onclick=()=>{copyText(C.wa[k]);toast('WhatsApp message copied');};ws.appendChild(b);});
 const g=$('#toolGrid');C.tools.forEach(t=>{const a=document.createElement('a');a.className='tool';a.href=t.url;a.target='_blank';a.rel='noopener';a.innerHTML='<h4>'+esc(t.name)+' <span class="a" aria-hidden="true">↗</span></h4><p>'+esc(t.desc)+'</p>';g.appendChild(a);});})();

/* precomputed counts */
const CT={};
P.forEach(p=>{const keys=['m|'+p.mode,'mt|'+p.mode+'|'+p.track,'mts|'+p.mode+'|'+p.track+'|'+p.subject,'mtsc|'+p.mode+'|'+p.track+'|'+p.subject+'|'+p.category,'mtc|'+p.mode+'|'+p.track+'|'+p.category];keys.forEach(k=>CT[k]=(CT[k]||0)+1);});
const cnt=k=>CT[k]||0;

function chipBtn(label,pressed,onclick,n){const b=document.createElement('button');b.className='chip';b.setAttribute('aria-pressed',!!pressed);b.innerHTML=esc(label)+(n!=null?' <span class="n">'+n+'</span>':'');b.onclick=onclick;return b;}
function buildMode(){const s=$('#modeSeg');s.innerHTML='';C.modes.forEach(m=>{const b=document.createElement('button');b.setAttribute('aria-pressed',m===st.mode);
  b.innerHTML=(m==='Teacher'?'👩‍🏫 ':'🎓 ')+m+' <span style="opacity:.6;font-weight:500">'+cnt('m|'+m)+'</span>';
  b.onclick=()=>{st.mode=m;st.track='all';st.sub='all';st.cat='all';st.shown=PAGE;buildMode();buildFacets();render();};s.appendChild(b);});}
function buildFacets(){
 const tracks=C.trackOrder.filter(t=>cnt('mt|'+st.mode+'|'+t)>0);
 const tc=$('#trackChips');tc.innerHTML='';tc.appendChild(chipBtn('All',st.track==='all',()=>{st.track='all';st.sub='all';st.cat='all';st.shown=PAGE;buildFacets();render();},cnt('m|'+st.mode)));
 tracks.forEach(t=>tc.appendChild(chipBtn(C.trackLabel[t]||t,st.track===t,()=>{st.track=t;st.sub='all';st.cat='all';st.shown=PAGE;buildFacets();render();},cnt('mt|'+st.mode+'|'+t))));
 const subF=p=>p.mode===st.mode&&(st.track==='all'||p.track===st.track);
 const subs=[...new Set(P.filter(subF).map(p=>p.subject))].sort();
 const sc=$('#subChips');sc.innerHTML='';sc.appendChild(chipBtn('All',st.sub==='all',()=>{st.sub='all';st.cat='all';st.shown=PAGE;buildFacets();render();},P.filter(subF).length));
 subs.forEach(su=>sc.appendChild(chipBtn(su,st.sub===su,()=>{st.sub=su;st.cat='all';st.shown=PAGE;buildFacets();render();},P.filter(p=>subF(p)&&p.subject===su).length)));
 const catF=p=>subF(p)&&(st.sub==='all'||p.subject===st.sub);
 const cats=[...new Set(P.filter(catF).map(p=>p.category))].sort();
 const cc=$('#catChips');cc.innerHTML='';cc.appendChild(chipBtn('All',st.cat==='all',()=>{st.cat='all';st.shown=PAGE;buildFacets();render();},P.filter(catF).length));
 cats.forEach(ca=>cc.appendChild(chipBtn(ca,st.cat===ca,()=>{st.cat=ca;st.shown=PAGE;buildFacets();render();},P.filter(p=>catF(p)&&p.category===ca).length)));
}
function setType(t,el){st.type=t;st.shown=PAGE;document.querySelectorAll('.tf').forEach(x=>x.setAttribute('aria-pressed',x===el));render();}
function toggleAsk(el){st.ask=!st.ask;st.shown=PAGE;el.setAttribute('aria-pressed',st.ask);render();}
function toggleFav(el){st.fav=!st.fav;st.shown=PAGE;el.setAttribute('aria-pressed',st.fav);render();}
function togglePop(el){st.pop=!st.pop;st.shown=PAGE;el.setAttribute('aria-pressed',st.pop);render();}
window.setType=setType;window.toggleAsk=toggleAsk;window.toggleFav=toggleFav;window.togglePop=togglePop;
function anyFilter(){return st.track!=='all'||st.sub!=='all'||st.cat!=='all'||st.type!=='all'||st.ask||st.fav||st.pop||st.q;}
function clearAll(){st.track='all';st.sub='all';st.cat='all';st.type='all';st.ask=false;st.fav=false;st.pop=false;st.shown=PAGE;$('#q').value='';
 var pc=$('#popChip');if(pc)pc.setAttribute('aria-pressed',false);
 document.querySelectorAll('.tf').forEach(x=>x.setAttribute('aria-pressed',x.dataset.type==='all'));$('#askChip').setAttribute('aria-pressed',false);$('#favChip').setAttribute('aria-pressed',false);buildFacets();render();}
$('#clr').onclick=clearAll;

function match(p){
 if(p.mode!==st.mode)return false;
 if(st.track!=='all'&&p.track!==st.track)return false;
 if(st.sub!=='all'&&p.subject!==st.sub)return false;
 if(st.cat!=='all'&&p.category!==st.cat)return false;
 if(st.type!=='all'&&p.output_type!==st.type)return false;
 if(st.ask&&!p.interactive)return false;
 if(st.pop&&!p.popular)return false;
 if(st.fav&&!favs.has(p.id))return false;
 if(st.q){const h=(p.title+' '+p.category+' '+p.track+' '+p.subject+' '+(p.what_you_get||'')+' '+(p.variables||[]).join(' ')).toLowerCase();return st.q.split(/\s+/).every(w=>h.includes(w));}
 return true;
}
function baseMatch(p){
 if(p.mode!==st.mode)return false;
 if(st.track!=='all'&&p.track!==st.track)return false;
 if(st.sub!=='all'&&p.subject!==st.sub)return false;
 if(st.cat!=='all'&&p.category!==st.cat)return false;
 if(st.q){const h=(p.title+' '+p.category+' '+p.track+' '+p.subject+' '+(p.what_you_get||'')+' '+(p.variables||[]).join(' ')).toLowerCase();return st.q.split(/\s+/).every(w=>h.includes(w));}
 return true;
}
function passToggles(p,except){
 if(except!=='type'&&st.type!=='all'&&p.output_type!==st.type)return false;
 if(except!=='ask'&&st.ask&&!p.interactive)return false;
 if(except!=='fav'&&st.fav&&!favs.has(p.id))return false;
 if(except!=='pop'&&st.pop&&!p.popular)return false;
 return true;
}
function refreshToggleCounts(){
 const base=P.filter(baseMatch);
 const nT=base.filter(p=>passToggles(p,'type')&&p.output_type==='text').length, nI=base.filter(p=>passToggles(p,'type')&&p.output_type==='image').length,
       nA=base.filter(p=>passToggles(p,'ask')&&p.interactive).length, nS=base.filter(p=>passToggles(p,'fav')&&favs.has(p.id)).length,
       nP=base.filter(p=>passToggles(p,'pop')&&p.popular).length;
 const set=(id,n)=>{const e=document.getElementById(id);if(e)e.textContent=n;};
 set('cText',nT);set('cImg',nI);set('cAsk',nA);set('cSaved',nS);set('cPop',nP);
 const dis=(sel,n,active)=>{const e=document.querySelector(sel);if(e)e.disabled=(n===0&&!active);};
 dis('#popChip',nP,st.pop);
 dis('.tf[data-type="text"]',nT,st.type==='text');dis('.tf[data-type="image"]',nI,st.type==='image');
 dis('#askChip',nA,st.ask);dis('#favChip',nS,st.fav);
}
const grid=$('#grid');
function cardEl(p,animate){
 const card=document.createElement('article');card.className='card';
 const vars=(p.variables||[]).slice(0,5).map(v=>'<span class="var">'+esc(v)+'</span>').join('');
 const isNew=p.added&&p.added>='2026-06-21';
 const badges=(p.popular?'<span class="badge pop">🔥 Popular</span>':'')+(isNew?'<span class="badge new">NEW</span>':'')+(p.interactive?'<span class="badge ask">💬 asks first</span>':'')+(p.output_type==='image'?'<span class="badge pic">🖼 photo</span>':'');
 const fav=favs.has(p.id);
 card.innerHTML='<div class="tagrow">'+badges+'<button class="star" aria-label="Save to favourites" aria-pressed="'+fav+'">'+(fav?'★':'☆')+'</button></div>'+
  '<div class="meta"><span class="ct">'+esc(p.subject)+' · '+esc(p.category)+'</span></div>'+
  '<h3>'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg"><b>YOU GET — </b>'+esc(p.what_you_get)+'</p>':'')+
  (vars?'<div class="vars">'+vars+'</div>':'')+
  '<div class="cbar"><button class="copy" title="Copy the prompt text">Copy</button><button class="open" title="Copy &amp; open '+AINAME[st.ai||'chatgpt']+'">Open ↗</button><button class="view" title="Read the full prompt first">Preview</button></div>';
 const cp=card.querySelector('.copy');
 cp.onclick=()=>{const done=()=>{cp.classList.add('done');cp.textContent='✓ Copied!';pushRecent(p.id);toast('Prompt copied — paste it into your AI');setTimeout(()=>{cp.classList.remove('done');cp.textContent='Copy';},1600);};
  if(BODIES[p.id]){copyText(BODIES[p.id]);done();}else{cp.textContent='Copying…';getBody(p.id).then(b=>{if(b&&b.indexOf('could not load')===-1){copyText(b);done();}else{cp.textContent='Copy';toast('Could not load the prompt — please refresh.');}});}};
 card.querySelector('.open').onclick=()=>openAI(p.id);
 card.querySelector('.view').onclick=()=>openModal(p);
 const star=card.querySelector('.star');
 star.onclick=()=>{if(favs.has(p.id)){favs.delete(p.id);}else{favs.add(p.id);}lset('ps-fav',[...favs]);const on=favs.has(p.id);star.setAttribute('aria-pressed',on);star.textContent=on?'★':'☆';if(st.fav)render();};
 if(animate){card.classList.add('reveal');card.style.animationDelay=(animate*0.03)+'s';}
 return card;
}
function render(){
 const items=P.filter(match);
 refreshToggleCounts();
 $('#clr').classList.toggle('show',anyFilter());
 $('#shown').textContent=Math.min(st.shown,items.length)+' / '+items.length+' shown';
 grid.innerHTML='';
 if(!items.length){
  if(st.fav&&favs.size===0){grid.innerHTML='<div class="empty">No saved prompts yet.<div class="sum">Tap the ☆ on any prompt to keep it here.</div><button class="btn solid" onclick="window.__clear()">Browse all prompts</button></div>';$('#more').innerHTML='';return;}
  const parts=[st.track!=='all'?st.track:'',st.sub!=='all'?st.sub:'',st.cat!=='all'?st.cat:'',st.type!=='all'?st.type:'',st.ask?'asks-first':'',st.pop?'popular':'',st.fav?'saved':''].filter(Boolean).join(' · ');
  const sug=(C.contact?'mailto:'+C.contact.email+'?subject='+encodeURIComponent('Prompt request: '+(st.q||parts||'(idea)')):'#');
  grid.innerHTML='<div class="empty">No prompts match.<div class="sum">'+(parts?'Filters: '+esc(parts):'')+'</div><button class="btn solid" onclick="window.__clear()">Clear all filters</button> <a class="btn line" href="'+sug+'">✦ Suggest this prompt</a></div>';
  $('#more').innerHTML='';return;
 }
 const fr=document.createDocumentFragment();
 items.slice(0,st.shown).forEach((p,i)=>fr.appendChild(cardEl(p,i<9?i:0)));
 grid.appendChild(fr);
 const rem=items.length-st.shown;
 if(rem>0){const b=document.createElement('button');b.className='btn line';b.textContent='Show '+Math.min(PAGE,rem)+' more ('+rem+' left)';
   b.onclick=()=>{const prev=st.shown;st.shown+=PAGE;const frag=document.createDocumentFragment();items.slice(prev,st.shown).forEach(p=>frag.appendChild(cardEl(p,0)));grid.appendChild(frag);
     const left=items.length-st.shown;if(left>0){b.textContent='Show '+Math.min(PAGE,left)+' more ('+left+' left)';}else{b.remove();}$('#shown').textContent=Math.min(st.shown,items.length)+' / '+items.length+' shown';};
   $('#more').innerHTML='';$('#more').appendChild(b);}else{$('#more').innerHTML='';}
}
window.__clear=clearAll;

/* modal with focus trap + history */
const modal=$('#modal');let lastFocus=null;
async function openModal(p){
 lastFocus=document.activeElement;
 const vars=(p.variables||[]).map(v=>'<span class="var">'+esc(v)+'</span>').join(' ');
 const lvls=(p.level||[]).map(l=>'<span class="badge">'+esc(l)+'</span>').join(' ');
 const badges=(p.interactive?'<span class="badge ask">💬 asks you first</span> ':'')+(p.output_type==='image'?'<span class="badge pic">🖼 photo-aware</span> ':'');
 $('#sheet').innerHTML='<button class="x" id="mx" aria-label="Close">✕</button>'+
  '<div class="meta"><span class="ct">'+esc(p.mode)+' · '+esc(p.track)+' · '+esc(p.subject)+'</span></div>'+
  '<div class="tagrow" style="margin:6px 0">'+badges+'</div>'+
  '<h3 id="sheetTitle">'+esc(p.title)+'</h3>'+(p.what_you_get?'<p class="yg">'+esc(p.what_you_get)+'</p>':'')+
  '<div class="lab">'+esc(p.category)+(lvls?' · best for':'')+'</div>'+(lvls?'<div class="tagrow">'+lvls+'</div>':'')+
  (vars?'<div class="lab">Fill in these blanks</div><p class="hint">Replace each [BRACKET] with your own detail — or delete it and just attach your question.</p><div class="vars">'+vars+'</div>':'')+
  (p.output_type==='image'?'<p class="hint">📎 To attach a photo: in ChatGPT / Claude / Gemini tap the paperclip or + icon, choose your photo, then paste this prompt and send.</p>':'')+
  (p.sample?'<details class="sample"><summary>👀 See an example answer</summary><pre class="full">'+esc(p.sample)+'</pre></details>':'')+
  '<div class="lab">The prompt</div><pre class="full" id="mfull">Loading…</pre>'+
  '<div class="cbar"><button class="copy" id="mc" style="flex:1">Copy prompt</button><button class="open" id="mo">Open ↗</button></div>';
 modal.classList.add('open');document.body.style.overflow='hidden';
 if(!(history.state&&history.state.modal))history.pushState({modal:p.id},'','#p/'+p.id);
 const body=await getBody(p.id);const full=$('#mfull');if(full)full.textContent=body;
 $('#mc').onclick=()=>{copyText(body);pushRecent(p.id);toast('Prompt copied');const b=$('#mc');b.classList.add('done');b.textContent='✓ Copied!';setTimeout(()=>{b.classList.remove('done');b.textContent='Copy prompt';},1600);};
 $('#mo').onclick=()=>{pushRecent(p.id);openAI(p.id);};
 $('#mx').onclick=closeModal;
 const mx=$('#mx');if(mx)mx.focus();
}
function closeModal(){if(!modal.classList.contains('open'))return;modal.classList.remove('open');document.body.style.overflow='';if(lastFocus&&lastFocus.focus)lastFocus.focus();if(history.state&&history.state.modal)history.back();}
modal.onclick=e=>{if(e.target===modal)closeModal();};
window.addEventListener('popstate',()=>{if(modal.classList.contains('open')){modal.classList.remove('open');document.body.style.overflow='';if(lastFocus&&lastFocus.focus)lastFocus.focus();}});
document.addEventListener('keydown',e=>{
 if(!modal.classList.contains('open'))return;
 if(e.key==='Escape'){closeModal();return;}
 if(e.key==='Tab'){const f=modal.querySelectorAll('button, a, [tabindex]');if(!f.length)return;const first=f[0],last=f[f.length-1];
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}
});

let qt;$('#q').addEventListener('input',e=>{clearTimeout(qt);qt=setTimeout(()=>{st.q=e.target.value.trim().toLowerCase();st.shown=PAGE;render();},120);});
/* deep-link to a prompt via #p/ID */
(function(){const m=location.hash.match(/^#p\/(.+)$/);if(m){const p=P.find(x=>x.id===m[1]);if(p){setTimeout(()=>openModal(p),300);}else{setTimeout(()=>{toast('That prompt link is no longer available.');try{history.replaceState(null,'',location.pathname);}catch(e){}},400);}}})();
/* Filters collapse toggle (collapsed by default on phones) */
(function(){const ctrl=document.querySelector('.controls'),ft=$('#filtToggle');if(!ft)return;
 ft.onclick=()=>{const c=ctrl.classList.toggle('collapsed');ft.setAttribute('aria-expanded',String(!c));};
 if(window.matchMedia&&window.matchMedia('(max-width:760px)').matches){ctrl.classList.add('collapsed');ft.setAttribute('aria-expanded','false');}})();
/* Share */
(function(){const b=$('#shareBtn');if(!b)return;b.onclick=async()=>{const data={title:C.brand,text:C.count+'+ free AI prompts for teachers & students — JEE, NEET, Olympiad & Boards.',url:C.site};
 if(navigator.share){try{await navigator.share(data);}catch(e){}}else{copyText(C.site);toast('Link copied — paste it into WhatsApp 💚');}};})();
buildMode();buildFacets();buildAI();render();
})();}
</script>
</body>
</html>
"""

out=(TEMPLATE.replace("__TITLE__",esc(TITLE)).replace("__DESC__",esc(DESC)).replace("__BRAND__",esc(BRAND))
 .replace("__AUTHOR__",esc(AUTHOR)).replace("__ROLE__",esc(ROLE)).replace("__BUILD__",BUILD)
 .replace("__COUNT__",str(COUNT)).replace("__SITE__",SITE_URL).replace("__FAVICON__",FAVICON)
 .replace("__JSONLD__",json.dumps(JSONLD,ensure_ascii=False))
 .replace("__STATIC__",STATIC_CARDS)
 .replace("__DATA__",jsemb(INDEX)).replace("__CFG__",jsemb(CONFIG)))
open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(out)
json.dump(BODIES,open(os.path.join(HERE,"bodies.json"),"w",encoding="utf-8"),ensure_ascii=False)

# robots.txt + sitemap.xml
open(os.path.join(HERE,"robots.txt"),"w").write("User-agent: *\nAllow: /\nSitemap: "+SITE_URL+"sitemap.xml\n")
open(os.path.join(HERE,"sitemap.xml"),"w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 f'  <url><loc>{SITE_URL}</loc><lastmod>{BUILD}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n</urlset>\n')

# og-cover.svg (rasterise to og-cover.png separately)
OG=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#f7f1e6"/>
<rect x="0" y="0" width="1200" height="12" fill="#1c4a3a"/>
<text x="80" y="138" font-family="Hanken Grotesk,Arial,sans-serif" font-size="23" letter-spacing="3" fill="#8f4426" font-weight="700">FREE · FOR TEACHERS &amp; STUDENTS</text>
<text x="76" y="298" font-family="Fraunces,Georgia,serif" font-size="108" font-weight="600" fill="#211d16">{COUNT}+ premium</text>
<text x="76" y="410" font-family="Fraunces,Georgia,serif" font-size="108" font-weight="600" fill="#211d16">AI prompts <tspan font-style="italic" fill="#8f4426">for you</tspan></text>
<text x="80" y="500" font-family="Newsreader,Georgia,serif" font-size="32" fill="#463f33">JEE · NEET · Olympiad · Boards — interview-first &amp; photo-aware</text>
<text x="80" y="568" font-family="Hanken Grotesk,Arial,sans-serif" font-size="25" fill="#5a5347">Prompt Studio · by {AUTHOR}</text>
<circle cx="1108" cy="92" r="40" fill="none" stroke="#1c4a3a" stroke-width="3"/>
<text x="1108" y="107" font-family="Fraunces,Georgia,serif" font-style="italic" font-size="42" fill="#1c4a3a" text-anchor="middle">P</text>
</svg>'''
open(os.path.join(HERE,"og-cover.svg"),"w",encoding="utf-8").write(OG)

# docs
md=[f"# {BRAND}","",f"_{COUNT}+ premium AI prompts for teachers & students — curated by {AUTHOR}. Built {BUILD}._",""]
by={}
for p in prompts: by.setdefault((p["mode"],p["track"],p["subject"]),[]).append(p)
for key in sorted(by.keys()):
 m,t,s=key; md.append(f"\n## {m} · {t} · {s}  ({len(by[key])})\n")
 for p in by[key]:
  md.append(f"### {p['title']}")
  if p.get("what_you_get"): md.append(f"You get: {p['what_you_get']}")
  md.append("\n```\n"+p["prompt"].strip()+"\n```\n")
open(os.path.join(HERE,"prompt-pack.md"),"w",encoding="utf-8").write("\n".join(md))
wt=["="*60,f"  {BRAND} — WhatsApp messages","="*60,""]
for k,v in WA.items(): wt+=[f"\n----- {k} -----\n",v,""]
wt+=["\nLive: "+SITE_URL]
open(os.path.join(HERE,"WHATSAPP-MESSAGES.txt"),"w",encoding="utf-8").write("\n".join(wt))

print(f"index.html {os.path.getsize(os.path.join(HERE,'index.html'))//1024}KB · bodies.json {os.path.getsize(os.path.join(HERE,'bodies.json'))//1024}KB · {COUNT} prompts · robots+sitemap+og-svg written")
