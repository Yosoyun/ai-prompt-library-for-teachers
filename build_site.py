#!/usr/bin/env python3
"""Build the self-contained 'Prompt Studio for Teachers' site from data/prompts.json.
Run:  python3 build_site.py
Generates: index.html (single file, offline-capable), prompt-pack.md, WHATSAPP-MESSAGES.txt
"""
import json, html, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
prompts = json.load(open(os.path.join(HERE, "data", "prompts.json"), encoding="utf-8"))

# ---------------- CONFIG (single source of truth) ----------------
AUTHOR   = "Indrajeet Yadav"
ROLE     = "Maths Faculty"
BRAND    = "Prompt Studio for Teachers"
TAGLINE  = "Ready-to-use AI prompts that do a teacher's busywork in seconds."
BUILD    = datetime.date.today().isoformat()

CONTACT = {
    "email": "indrajeetsirallen@gmail.com",
    "wa_num": "918072965053",            # digits only, for wa.me
    "wa_show": "+91 80729 65053",
    "insta": "indrajeetsirallen",
}
# Paste a Google Form URL here when ready; empty -> feedback uses email + WhatsApp.
FEEDBACK_FORM_URL = ""

# Other free tools by the author (verified live)
TOOLS = [
    {"emoji":"🧮","name":"Maths Prompt Studio","desc":"136+ AI prompts for maths teachers — solutions, papers, worksheets, DPPs.","url":"https://yosoyun.github.io/math-prompt-studio/"},
    {"emoji":"📚","name":"Ranker Masterbooks","desc":"ARC & LIMITS — 200 original multi-method problems, Python-verified.","url":"https://yosoyun.github.io/ranker-masterbooks/"},
    {"emoji":"🏛️","name":"Andreescu Library","desc":"A searchable guide to every book by Titu Andreescu.","url":"https://yosoyun.github.io/andreescu-library/"},
    {"emoji":"♾️","name":"LIMITS Masterbook","desc":"100 ranker-level limit problems (JEE Advanced / Olympiad).","url":"https://limits-masterbook.vercel.app"},
    {"emoji":"🎯","name":"AMC 8 Math App","desc":"Practice app for the AMC 8 mathematics competition.","url":"https://amc8-math-app-two.vercel.app"},
]

CATEGORY_ORDER = [
    "Solutions & Worked Examples", "Practice, DPP & Tests", "Question Papers & Assessment",
    "Concepts, Proofs & Theory", "Doubt-Solving & Remedial", "Visual & Diagram Maths",
    "Lesson Planning & Notes", "Student Feedback & Mentoring", "WhatsApp & Parent Communication",
    "Content & Social Media", "AI Productivity & Workflow", "Prompt-Writing & Meta",
]
CAT_META = {
    "Solutions & Worked Examples": ("✍️","Step-by-step solutions, multi-method answers, worked pages."),
    "Practice, DPP & Tests": ("📝","DPPs, daily practice, drills and graded assignments."),
    "Question Papers & Assessment": ("📄","Exam papers, board tests, answer keys and rubrics."),
    "Concepts, Proofs & Theory": ("📐","Explain concepts, prove theorems, build intuition."),
    "Doubt-Solving & Remedial": ("🔧","Fix misconceptions and repair weak foundations."),
    "Visual & Diagram Maths": ("📊","Graphs, diagrams, figures and visual explanations."),
    "Lesson Planning & Notes": ("🗂️","Lesson plans, revision sheets, notes and workflow."),
    "Student Feedback & Mentoring": ("🧑‍🏫","Feedback, mentoring and personalised guidance."),
    "WhatsApp & Parent Communication": ("💬","Parent updates and clean WhatsApp-ready messages."),
    "Content & Social Media": ("🎬","YouTube, Instagram and post ideas for educators."),
    "AI Productivity & Workflow": ("⚡","Summaries, custom instructions and time-savers."),
    "Prompt-Writing & Meta": ("🧩","Build and sharpen your own prompts."),
}
LEVELS = ["School (6–10)", "Boards (11–12)", "JEE / NEET", "Olympiad", "Any"]

# ---------------- normalise prompts (defensive to old/new schema) ----------------
def varlist(v):
    if isinstance(v, list): return [str(x).strip() for x in v if str(x).strip()]
    if not v: return []
    import re
    return [x.strip() for x in re.split(r"[,\n]", str(v)) if x.strip()]

norm = []
for i, p in enumerate(prompts, 1):
    cat = p.get("category", "AI Productivity & Workflow")
    if cat not in CATEGORY_ORDER: cat = "AI Productivity & Workflow"
    lv = p.get("level") or ["Any"]
    if isinstance(lv, str): lv = [lv]
    lv = [x for x in lv if x in LEVELS] or ["Any"]
    norm.append({
        "id": p.get("id", f"P{i:03d}"),
        "title": (p.get("title") or "Untitled prompt").strip(),
        "category": cat,
        "level": lv,
        "output_type": "image" if str(p.get("output_type","")).lower()=="image" else "text",
        "use_case": (p.get("use_case") or "").strip(),
        "what_you_get": (p.get("what_you_get") or p.get("use_case") or "").strip(),
        "variables": varlist(p.get("variables", [])),
        "prompt": (p.get("prompt") or "").strip(),
        "tool": (p.get("tool") or "Any").strip(),
    })
prompts = norm
COUNT = len(prompts)

counts = {c: 0 for c in CATEGORY_ORDER}
for p in prompts: counts[p["category"]] += 1
used_cats = [c for c in CATEGORY_ORDER if counts[c] > 0]

# ---------------- WhatsApp share messages ----------------
WA = {
"Invite (English)": """🎓 *""" + BRAND + """*  —  free AI prompts for teachers

""" + str(COUNT) + """ ready-to-use, copy-paste prompts that save hours every day — solutions, DPPs, question papers, doubt-solving, lesson plans, parent & WhatsApp messages, content and more.

✅ 100% copy-paste. Works on ChatGPT, Claude or Gemini (free versions too).
🧩 Open → pick a prompt → fill the [BLANKS] → paste into the AI.

👉 https://yosoyun.github.io/ai-prompt-library-for-teachers/

Made for teachers, by """ + AUTHOR + """.""",

"How to use it daily (English)": """📌 *How to use """ + BRAND + """ every day*

1️⃣ Open the link & bookmark it on your phone.
2️⃣ Tap *Start here* once to see a 60-second example.
3️⃣ Pick a category (DPP, Question Paper, Doubt-Solving…) or search.
4️⃣ Tap *Copy*, paste into ChatGPT / Claude / Gemini.
5️⃣ Replace the [BRACKETS] — e.g. [TOPIC] → Integration, [GRADE] → Class 12.
6️⃣ Send. Every answer comes signed so students can reach the teacher.

💡 Try just *one* prompt a day:
• Morning — today's DPP / warm-up.
• Before class — a quick lesson or board plan.
• Doubt time — a step-by-step solution.
• Evening — a WhatsApp note or a post.

👉 https://yosoyun.github.io/ai-prompt-library-for-teachers/""",

"Invite (Hindi)": """🎓 *""" + BRAND + """* — शिक्षकों के लिए मुफ़्त AI प्रॉम्प्ट

रोज़ घंटों बचाने वाले """ + str(COUNT) + """ तैयार प्रॉम्प्ट — हल, DPP, प्रश्न-पत्र, डाउट सॉल्विंग, लेसन प्लान, पैरेंट/WhatsApp मैसेज और भी बहुत कुछ।

✅ पूरी तरह कॉपी-पेस्ट। ChatGPT, Claude या Gemini (फ्री वर्ज़न भी) पर चलता है।
🧩 खोलें → प्रॉम्प्ट चुनें → [BRACKETS] भरें → AI में पेस्ट करें।

👉 https://yosoyun.github.io/ai-prompt-library-for-teachers/

शिक्षकों के लिए — """ + AUTHOR + """ द्वारा।""",
}

# ---------------- embeds ----------------
def esc(s): return html.escape(s or "", quote=True)
def jsemb(obj): return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

CONFIG = {
    "brand": BRAND, "author": AUTHOR, "role": ROLE, "tagline": TAGLINE, "build": BUILD,
    "count": COUNT, "contact": CONTACT, "form": FEEDBACK_FORM_URL, "tools": TOOLS,
    "catOrder": used_cats, "catMeta": {c: CAT_META[c] for c in used_cats},
    "levels": LEVELS, "wa": WA,
}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="description" content="__COUNT__ free, copy-paste AI prompts for teachers — solutions, DPPs, question papers, doubt-solving, lesson plans and more. Works with ChatGPT, Claude and Gemini."/>
<meta name="theme-color" content="#0a0b14"/>
<title>__BRAND__ · __COUNT__ free AI prompts for teachers</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,800;1,9..144,500&family=Hanken+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Caveat:wght@600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#070811; --bg-soft:#0c0e1b; --ink:#eef0fb; --ink-dim:#a6abc8; --ink-faint:#6f7596;
  --line:rgba(255,255,255,.10); --line-2:rgba(255,255,255,.06);
  --glass:rgba(255,255,255,.045); --glass-2:rgba(255,255,255,.07); --glass-hi:rgba(255,255,255,.10);
  --a1:#7c83ff; --a2:#b06cff; --a3:#37e0d6; --warm:#ffb454; --green:#46e0a0; --rose:#ff7aa8;
  --grad:linear-gradient(135deg,#7c83ff,#b06cff 60%,#ff7aa8);
  --shadow:0 1px 0 rgba(255,255,255,.06) inset, 0 24px 60px -28px rgba(0,0,0,.85);
  --r:20px; --r-sm:13px; --maxw:1180px;
  --f-disp:"Fraunces",Georgia,serif; --f-ui:"Hanken Grotesk",-apple-system,sans-serif; --f-mono:"JetBrains Mono",ui-monospace,monospace;
}
html[data-theme="light"]{
  --bg:#f3f4fb; --bg-soft:#fbfbff; --ink:#15172a; --ink-dim:#4a5072; --ink-faint:#878da8;
  --line:rgba(20,22,50,.12); --line-2:rgba(20,22,50,.07);
  --glass:rgba(255,255,255,.62); --glass-2:rgba(255,255,255,.78); --glass-hi:rgba(255,255,255,.92);
  --shadow:0 1px 0 rgba(255,255,255,.7) inset, 0 22px 50px -30px rgba(40,40,90,.5);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-ui);line-height:1.55;
  font-size:16px;letter-spacing:.1px;overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
::selection{background:rgba(124,131,255,.35)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}

/* aurora backdrop */
.aurora{position:fixed;inset:-20% -10%;z-index:-2;filter:blur(60px) saturate(130%);opacity:.55;pointer-events:none}
.aurora span{position:absolute;border-radius:50%;mix-blend-mode:screen;animation:drift 26s ease-in-out infinite}
html[data-theme="light"] .aurora{opacity:.4;mix-blend-mode:normal}
.aurora .b1{width:46vw;height:46vw;left:-6%;top:-8%;background:radial-gradient(circle,#5b62ff,transparent 62%)}
.aurora .b2{width:42vw;height:42vw;right:-6%;top:2%;background:radial-gradient(circle,#b06cff,transparent 62%);animation-delay:-6s}
.aurora .b3{width:40vw;height:40vw;left:18%;top:40%;background:radial-gradient(circle,#37e0d6,transparent 64%);animation-delay:-12s}
.aurora .b4{width:38vw;height:38vw;right:6%;bottom:-6%;background:radial-gradient(circle,#ff7aa8,transparent 64%);animation-delay:-18s}
@keyframes drift{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(4%,5%) scale(1.08)}66%{transform:translate(-4%,-3%) scale(.95)}}
.grain{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.05;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
@media (prefers-reduced-motion: reduce){.aurora span{animation:none}*{scroll-behavior:auto!important}}

/* glass primitive */
.glass{background:var(--glass);backdrop-filter:blur(22px) saturate(150%);-webkit-backdrop-filter:blur(22px) saturate(150%);
  border:1px solid var(--line);box-shadow:var(--shadow)}

/* top nav */
header.nav{position:sticky;top:0;z-index:60;border-bottom:1px solid var(--line-2);
  background:color-mix(in srgb,var(--bg) 72%, transparent);backdrop-filter:blur(16px)}
.nav .row{display:flex;align-items:center;gap:18px;height:62px}
.brand{display:flex;align-items:center;gap:11px;font-weight:800;font-size:16px;letter-spacing:-.2px;white-space:nowrap}
.brand .mark{width:30px;height:30px;border-radius:9px;background:var(--grad);display:grid;place-items:center;
  font-family:var(--f-disp);font-weight:800;color:#fff;box-shadow:0 6px 18px -6px rgba(124,131,255,.8)}
.nav nav{display:flex;gap:4px;margin-left:auto}
.nav nav a{padding:8px 13px;border-radius:10px;color:var(--ink-dim);font-weight:600;font-size:14px;transition:.16s}
.nav nav a:hover{color:var(--ink);background:var(--glass)}
.iconbtn{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;cursor:pointer;
  background:var(--glass);border:1px solid var(--line);color:var(--ink);transition:.16s}
.iconbtn:hover{background:var(--glass-2);transform:translateY(-1px)}
@media(max-width:780px){.nav nav{display:none}}

/* hero */
.hero{position:relative;padding:74px 0 38px;text-align:center}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;
  font-size:12.5px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--ink-dim);
  background:var(--glass);border:1px solid var(--line);margin-bottom:22px}
.eyebrow .dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 10px var(--green)}
h1.title{font-family:var(--f-disp);font-weight:800;font-size:clamp(38px,7vw,76px);line-height:1.02;
  letter-spacing:-1.5px;margin:0 0 18px}
h1.title em{font-style:italic;font-weight:500;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.lede{max-width:640px;margin:0 auto 28px;color:var(--ink-dim);font-size:clamp(16px,2.2vw,19px)}
.cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 22px;border-radius:13px;font-weight:700;font-size:15px;
  cursor:pointer;border:1px solid transparent;transition:.18s;font-family:var(--f-ui)}
.btn.primary{background:var(--grad);color:#fff;box-shadow:0 14px 34px -12px rgba(124,131,255,.8)}
.btn.primary:hover{transform:translateY(-2px);box-shadow:0 20px 44px -12px rgba(176,108,255,.9)}
.btn.ghost{background:var(--glass);border-color:var(--line);color:var(--ink)}
.btn.ghost:hover{background:var(--glass-2);transform:translateY(-2px)}
.stats{display:flex;gap:30px;justify-content:center;flex-wrap:wrap;margin-top:40px}
.stat{text-align:center}
.stat b{display:block;font-family:var(--f-disp);font-size:30px;font-weight:800;letter-spacing:-.5px}
.stat span{font-size:12.5px;color:var(--ink-faint);text-transform:uppercase;letter-spacing:.6px;font-weight:600}

section{padding:46px 0}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:24px;flex-wrap:wrap}
.sec-head h2{font-family:var(--f-disp);font-weight:700;font-size:clamp(26px,4vw,40px);letter-spacing:-.8px;margin:0}
.sec-head p{color:var(--ink-dim);margin:6px 0 0;max-width:520px}
.kick{font-size:12.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--a1);margin-bottom:8px}

/* start-here */
.start{border-radius:var(--r);padding:30px;display:grid;grid-template-columns:1.1fr 1fr;gap:30px}
.start h3{font-family:var(--f-disp);font-size:24px;font-weight:700;margin:0 0 6px}
.steps{counter-reset:s;display:grid;gap:14px;margin-top:8px}
.steps li{list-style:none;display:flex;gap:13px;align-items:flex-start}
.steps li::before{counter-increment:s;content:counter(s);flex:none;width:28px;height:28px;border-radius:9px;
  background:var(--grad);color:#fff;font-weight:800;font-size:13px;display:grid;place-items:center;box-shadow:0 6px 16px -6px rgba(124,131,255,.8)}
.steps li b{color:var(--ink)} .steps li span{color:var(--ink-dim)}
.tools-pick{display:flex;flex-direction:column;gap:11px}
.tools-pick .lbl{font-size:13px;color:var(--ink-faint);font-weight:600;text-transform:uppercase;letter-spacing:.6px}
.ai-row{display:flex;gap:10px;flex-wrap:wrap}
.ai-chip{display:flex;align-items:center;gap:9px;padding:11px 15px;border-radius:12px;font-weight:700;font-size:14px;
  background:var(--glass);border:1px solid var(--line);transition:.16s}
.ai-chip:hover{transform:translateY(-2px);border-color:var(--a1);background:var(--glass-2)}
.ai-chip i{width:9px;height:9px;border-radius:50%;background:var(--green)}
.example{margin-top:6px;border-radius:var(--r-sm);padding:15px 16px;background:var(--bg-soft);border:1px solid var(--line-2)}
.example .q{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-dim);white-space:pre-wrap}
.example .tag{font-family:var(--f-ui);display:inline-block;font-size:11px;font-weight:700;color:var(--a3);margin-bottom:6px;text-transform:uppercase;letter-spacing:.6px}
@media(max-width:760px){.start{grid-template-columns:1fr;padding:22px}}

/* category shelves */
.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.cat-card{border-radius:var(--r-sm);padding:18px;cursor:pointer;transition:.18s;position:relative;overflow:hidden}
.cat-card:hover{transform:translateY(-3px);border-color:var(--line);background:var(--glass-2)}
.cat-card .em{font-size:24px}
.cat-card h4{margin:10px 0 4px;font-size:16px;font-weight:700}
.cat-card p{margin:0;color:var(--ink-dim);font-size:13px;line-height:1.45}
.cat-card .ct{position:absolute;top:16px;right:16px;font-family:var(--f-mono);font-size:12px;color:var(--ink-faint);
  background:var(--glass);border:1px solid var(--line);padding:3px 9px;border-radius:999px}

/* library controls */
.controls{position:sticky;top:62px;z-index:40;padding:14px 0;background:color-mix(in srgb,var(--bg) 80%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line-2)}
.searchbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;font-family:var(--f-ui);font-size:15px;color:var(--ink);padding:13px 14px 13px 44px;border-radius:13px;
  background:var(--glass);border:1px solid var(--line);outline:none;transition:.16s}
.search input::placeholder{color:var(--ink-faint)}
.search input:focus{border-color:var(--a1);box-shadow:0 0 0 3px rgba(124,131,255,.18)}
.search svg{position:absolute;left:15px;top:50%;transform:translateY(-50%);stroke:var(--ink-faint)}
.shown{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-faint);white-space:nowrap}
.filters{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:11px}
.fgroup{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.fgroup .glabel{font-size:11px;color:var(--ink-faint);font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-right:2px}
.chip{white-space:nowrap;font-family:var(--f-ui);font-size:13px;font-weight:600;padding:7px 12px;border-radius:999px;cursor:pointer;
  background:var(--glass);border:1px solid var(--line);color:var(--ink-dim);transition:.14s}
.chip:hover{color:var(--ink);border-color:var(--a1)}
.chip.on{background:var(--grad);border-color:transparent;color:#fff;box-shadow:0 8px 20px -10px rgba(124,131,255,.9)}
.chip .n{opacity:.6;margin-left:5px;font-family:var(--f-mono);font-size:11px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;vertical-align:middle}
.dot.text{background:var(--green)} .dot.image{background:var(--warm)}

/* prompt grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;align-items:start;padding-top:22px}
.card{border-radius:var(--r);padding:18px;display:flex;flex-direction:column;gap:11px;transition:.18s;position:relative}
.card:hover{transform:translateY(-3px);border-color:var(--a1)}
.card .meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.pill{font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--glass-2);color:var(--ink-dim);border:1px solid var(--line-2)}
.pill.cat{color:var(--a1);background:rgba(124,131,255,.12);border-color:rgba(124,131,255,.2)}
.pill.sign{color:var(--a3);background:rgba(55,224,214,.1);border-color:rgba(55,224,214,.22)}
.card h3{font-size:17px;font-weight:700;line-height:1.28;margin:0}
.card .yg{color:var(--ink-dim);font-size:13.5px;margin:0}
.card .yg b{color:var(--ink);font-weight:600}
.vars{display:flex;flex-wrap:wrap;gap:5px}
.var{font-family:var(--f-mono);font-size:11px;color:var(--warm);background:rgba(255,180,84,.1);border:1px solid rgba(255,180,84,.22);padding:2px 7px;border-radius:6px}
.card .lvls{display:flex;gap:5px;flex-wrap:wrap}
.lv{font-size:11px;font-weight:600;color:var(--ink-faint);background:var(--glass);border:1px solid var(--line-2);padding:2px 8px;border-radius:6px}
.cardbar{display:flex;gap:8px;margin-top:auto;padding-top:4px}
.copy{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:11px;border-radius:11px;
  font-weight:700;font-size:13.5px;cursor:pointer;border:none;background:var(--grad);color:#fff;transition:.16s;font-family:var(--f-ui)}
.copy:hover{transform:translateY(-1px);filter:brightness(1.06)}
.copy.done{background:var(--green);color:#06301f}
.view{padding:11px 14px;border-radius:11px;background:var(--glass);border:1px solid var(--line);color:var(--ink-dim);font-weight:600;font-size:13px;cursor:pointer;transition:.16s}
.view:hover{color:var(--ink);border-color:var(--a1)}
.empty{text-align:center;color:var(--ink-faint);padding:70px 0;font-size:16px}

/* tools */
.tool-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.tool{border-radius:var(--r-sm);padding:18px;display:flex;gap:14px;align-items:flex-start;transition:.18s}
.tool:hover{transform:translateY(-3px);border-color:var(--a2)}
.tool .em{font-size:26px;flex:none}
.tool h4{margin:0 0 4px;font-size:15.5px;font-weight:700;display:flex;align-items:center;gap:7px}
.tool h4 .arr{color:var(--a1);transition:.16s} .tool:hover h4 .arr{transform:translate(3px,-3px)}
.tool p{margin:0;color:var(--ink-dim);font-size:13px;line-height:1.45}

/* contact / signature */
.contact{border-radius:var(--r);padding:32px;text-align:center}
.sigcard{max-width:560px;margin:0 auto;border-radius:var(--r-sm);padding:22px;background:var(--bg-soft);border:1px solid var(--line)}
.sigcard .who{font-family:var(--f-disp);font-size:22px;font-weight:700}
.sigcard .role{color:var(--ink-faint);font-size:14px;margin-bottom:16px}
.contact-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:6px}
.cbtn{display:inline-flex;align-items:center;gap:8px;padding:11px 16px;border-radius:12px;font-weight:700;font-size:14px;
  background:var(--glass);border:1px solid var(--line);transition:.16s}
.cbtn:hover{transform:translateY(-2px);border-color:var(--a1);background:var(--glass-2)}
.cbtn.wa{color:#25d366} .cbtn.ig{color:#e1306c} .cbtn.em{color:var(--a1)} .cbtn.fb{background:var(--grad);color:#fff;border-color:transparent}
.note{color:var(--ink-faint);font-size:13px;margin-top:16px}

/* WA share buttons */
.wa-share{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:18px}
.wabtn{display:inline-flex;align-items:center;gap:8px;padding:10px 15px;border-radius:11px;font-weight:700;font-size:13px;cursor:pointer;
  background:#25d366;color:#04391c;border:none;transition:.16s}
.wabtn:hover{transform:translateY(-2px);filter:brightness(.97)}
.wabtn.alt{background:var(--glass);color:var(--ink);border:1px solid var(--line)}

footer{border-top:1px solid var(--line-2);padding:34px 0 50px;text-align:center;color:var(--ink-faint);font-size:13.5px}
footer b{color:var(--ink-dim)} footer .hand{font-family:var(--f-disp);font-style:italic;color:var(--ink-dim)}

/* modal */
.modal{position:fixed;inset:0;z-index:90;display:none;align-items:center;justify-content:center;padding:20px;
  background:rgba(4,5,12,.6);backdrop-filter:blur(8px)}
.modal.open{display:flex}
.sheet{width:min(720px,100%);max-height:88vh;overflow:auto;border-radius:22px;padding:26px}
.sheet .x{position:absolute;top:16px;right:18px}
.sheet .meta{margin-bottom:10px}
.sheet h3{font-family:var(--f-disp);font-size:24px;font-weight:700;margin:6px 0 6px;letter-spacing:-.4px}
.sheet .yg{color:var(--ink-dim);margin:0 0 14px}
pre.full{white-space:pre-wrap;word-break:break-word;font-family:var(--f-mono);font-size:12.5px;line-height:1.6;
  color:var(--ink);background:var(--bg-soft);border:1px solid var(--line);border-radius:14px;padding:16px;margin:0 0 14px}
.sheet .label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--ink-faint);margin:12px 0 7px}

#toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(24px);opacity:0;z-index:100;
  background:var(--ink);color:var(--bg);padding:12px 20px;border-radius:12px;font-weight:700;font-size:14px;
  box-shadow:0 16px 40px rgba(0,0,0,.4);transition:.22s;pointer-events:none}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

.reveal{opacity:0;transform:translateY(16px);animation:rise .7s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
@media(max-width:560px){.hero{padding:52px 0 28px}.grid{grid-template-columns:1fr}.stats{gap:20px}}
</style>
</head>
<body>
<div class="aurora"><span class="b1"></span><span class="b2"></span><span class="b3"></span><span class="b4"></span></div>
<div class="grain"></div>

<header class="nav"><div class="wrap row">
  <a class="brand" href="#top"><span class="mark">P</span>__BRAND__</a>
  <nav>
    <a href="#start">Start here</a>
    <a href="#library">Library</a>
    <a href="#tools">More tools</a>
    <a href="#contact">Contact</a>
  </nav>
  <button class="iconbtn" id="theme" title="Toggle light / dark" aria-label="Toggle theme">🌙</button>
</div></header>

<a id="top"></a>
<section class="hero"><div class="wrap">
  <div class="eyebrow reveal"><span class="dot"></span> Free · For teachers · ChatGPT · Claude · Gemini</div>
  <h1 class="title reveal" style="animation-delay:.05s">__COUNT__ prompts that do your <em>busywork</em><br>in seconds.</h1>
  <p class="lede reveal" style="animation-delay:.12s">__TAGLINE__ Open one, fill the blanks, paste into any AI. Every answer comes <b style="color:var(--ink)">signed by you</b>, so students and parents can reach you.</p>
  <div class="cta reveal" style="animation-delay:.18s">
    <a class="btn primary" href="#library">Browse the library →</a>
    <a class="btn ghost" href="#start">New to AI? Start here</a>
  </div>
  <div class="stats reveal" style="animation-delay:.24s">
    <div class="stat"><b id="s-count">__COUNT__</b><span>Prompts</span></div>
    <div class="stat"><b id="s-cats">__NCATS__</b><span>Categories</span></div>
    <div class="stat"><b>100%</b><span>Copy-paste</span></div>
    <div class="stat"><b>Free</b><span>Forever</span></div>
  </div>
</div></section>

<section id="start"><div class="wrap">
  <div class="kick">Start here · 60 seconds</div>
  <div class="glass start">
    <div>
      <h3>Never used AI? You'll be a pro in a minute.</h3>
      <ol class="steps">
        <li><div><b>Open a free AI tool.</b> <span>Pick one on the right — no payment needed.</span></div></li>
        <li><div><b>Copy any prompt</b> <span>from the library below (one tap).</span></div></li>
        <li><div><b>Paste &amp; fill the [BLANKS]</b> <span>— e.g. [TOPIC] → Integration, [GRADE] → Class 12.</span></div></li>
        <li><div><b>Send.</b> <span>To solve a photo of a question, attach the image, then paste the prompt.</span></div></li>
      </ol>
    </div>
    <div class="tools-pick">
      <span class="lbl">Open a free AI tool</span>
      <div class="ai-row">
        <a class="ai-chip" href="https://chatgpt.com" target="_blank" rel="noopener"><i></i>ChatGPT</a>
        <a class="ai-chip" href="https://claude.ai" target="_blank" rel="noopener"><i></i>Claude</a>
        <a class="ai-chip" href="https://gemini.google.com" target="_blank" rel="noopener"><i></i>Gemini</a>
      </div>
      <div class="example">
        <span class="tag">Try this first</span>
        <div class="q">Act as a maths teacher. Solve this Class 10 question in 3 different
methods, each on a clean page, with a one-line "why this method" note.
Question: [PASTE OR ATTACH THE QUESTION]</div>
      </div>
      <span class="lbl" style="margin-top:4px">🟢 text prompt &nbsp;·&nbsp; 🟠 makes an image</span>
    </div>
  </div>
</div></section>

<section id="library"><div class="wrap">
  <div class="sec-head">
    <div><div class="kick">The Library</div><h2>Browse every prompt</h2>
      <p>Tap a category to filter, or search. Each prompt is copy-paste ready and auto-signed.</p></div>
  </div>
  <div class="cat-grid" id="catGrid"></div>
</div></section>

<div class="controls"><div class="wrap">
  <div class="searchbar">
    <div class="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
      <input id="q" type="search" placeholder="Search prompts — DPP, integration, doubt, question paper, WhatsApp…" autocomplete="off"/>
    </div>
    <span class="shown" id="shown"></span>
  </div>
  <div class="filters">
    <div class="fgroup" id="catChips"></div>
  </div>
  <div class="filters">
    <div class="fgroup"><span class="glabel">Level</span><span id="lvlChips"></span></div>
    <div class="fgroup"><span class="glabel">Type</span>
      <span class="chip type-f" data-type="all" onclick="setType('all',this)">All</span>
      <span class="chip type-f" data-type="text" onclick="setType('text',this)"><span class="dot text"></span> Text</span>
      <span class="chip type-f" data-type="image" onclick="setType('image',this)"><span class="dot image"></span> Image</span>
    </div>
  </div>
</div></div>

<div class="wrap"><div class="grid" id="grid"></div></div>

<section id="tools"><div class="wrap">
  <div class="sec-head"><div><div class="kick">More free tools</div><h2>Other projects by __AUTHOR__</h2>
    <p>More free, no-login resources for teachers and students.</p></div></div>
  <div class="tool-grid" id="toolGrid"></div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="kick">Stay in touch</div>
  <div class="glass contact">
    <h2 style="font-family:var(--f-disp);font-size:clamp(24px,4vw,36px);margin:0 0 6px;letter-spacing:-.6px">Feedback, problems or appreciation?</h2>
    <p style="color:var(--ink-dim);max-width:560px;margin:0 auto 22px">I'd love to hear how this helps your teaching — and what to add next.</p>
    <div class="sigcard">
      <div class="who">__AUTHOR__</div>
      <div class="role">__ROLE__</div>
      <div class="contact-row" id="contactRow"></div>
    </div>
    <div class="wa-share" id="waShare"></div>
    <p class="note">Tip: every prompt tells the AI to sign each answer with these details, so your students and parents can always reach you.</p>
  </div>
</div></section>

<footer><div class="wrap">
  <span class="hand">Made for teachers, everywhere.</span><br>
  <b>__BRAND__</b> · __COUNT__ free prompts · Built __BUILD__ · Created &amp; curated by <b>__AUTHOR__</b><br>
  Free to share — please keep the credit. 💜
</div></footer>

<div class="modal" id="modal"><div class="glass sheet" id="sheet"></div></div>
<div id="toast">Copied!</div>

<script id="DATA" type="application/json">__DATA__</script>
<script id="CFG" type="application/json">__CFG__</script>
<script>
const P = JSON.parse(document.getElementById('DATA').textContent);
const C = JSON.parse(document.getElementById('CFG').textContent);
const $ = s => document.querySelector(s);
const esc = s => (s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let state = {q:'', cat:'all', level:'all', type:'all'};

/* theme */
const themeBtn = $('#theme');
function applyTheme(t){document.documentElement.dataset.theme=t;themeBtn.textContent=t==='dark'?'🌙':'☀️';try{localStorage.setItem('ps-theme',t)}catch(e){}}
applyTheme((()=>{try{return localStorage.getItem('ps-theme')||'dark'}catch(e){return 'dark'}})());
themeBtn.onclick=()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');

/* clipboard (works on file:// and https) */
function copyText(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(()=>fb(t));}return Promise.resolve(fb(t));}
function fb(t){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.top='-9999px';document.body.appendChild(a);a.focus();a.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(a);}
let tT;function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(tT);tT=setTimeout(()=>t.classList.remove('show'),1500);}

/* contact links */
function contactLinks(){
  const c=C.contact;
  return {
    email:`mailto:${c.email}?subject=${encodeURIComponent('Feedback — '+C.brand)}`,
    wa:`https://wa.me/${c.wa_num}`,
    ig:`https://instagram.com/${c.insta}`
  };
}
(function renderContact(){
  const L=contactLinks(), row=$('#contactRow');
  let h=`<a class="cbtn em" href="${L.email}">📧 ${C.contact.email}</a>`+
        `<a class="cbtn wa" href="${L.wa}" target="_blank" rel="noopener">💬 WhatsApp</a>`+
        `<a class="cbtn ig" href="${L.ig}" target="_blank" rel="noopener">📸 @${C.contact.insta}</a>`;
  if(C.form) h+=`<a class="cbtn fb" href="${C.form}" target="_blank" rel="noopener">📝 Send feedback</a>`;
  else h+=`<a class="cbtn fb" href="${L.email}">📝 Send feedback</a>`;
  row.innerHTML=h;
  // WA share
  const ws=$('#waShare');
  Object.keys(C.wa).forEach((k,i)=>{const b=document.createElement('button');b.className='wabtn'+(i?' alt':'');
    b.innerHTML=(i?'📋 ':'💬 ')+'Copy: '+k;b.onclick=()=>{copyText(C.wa[k]);toast('WhatsApp message copied — paste into your group');};ws.appendChild(b);});
})();

/* tools */
(function(){const g=$('#toolGrid');C.tools.forEach(t=>{const a=document.createElement('a');a.className='glass tool';a.href=t.url;a.target='_blank';a.rel='noopener';
  a.innerHTML=`<span class="em">${t.emoji}</span><div><h4>${esc(t.name)} <span class="arr">↗</span></h4><p>${esc(t.desc)}</p></div>`;g.appendChild(a);});})();

/* category shelves + chips */
function catCount(c){return P.filter(p=>p.category===c).length;}
(function(){
  const cg=$('#catGrid');
  C.catOrder.forEach(c=>{const m=C.catMeta[c];const d=document.createElement('div');d.className='glass cat-card';
    d.innerHTML=`<span class="ct">${catCount(c)}</span><div class="em">${m[0]}</div><h4>${esc(c)}</h4><p>${esc(m[1])}</p>`;
    d.onclick=()=>{setCat(c);document.querySelector('.controls').scrollIntoView({behavior:'smooth',block:'start'});};cg.appendChild(d);});
  const cc=$('#catChips');
  const all=document.createElement('span');all.className='chip on';all.dataset.cat='all';all.innerHTML='★ All <span class="n">'+P.length+'</span>';
  all.onclick=()=>setCat('all');cc.appendChild(all);
  C.catOrder.forEach(c=>{const s=document.createElement('span');s.className='chip';s.dataset.cat=c;
    s.innerHTML=`${C.catMeta[c][0]} ${esc(c)} <span class="n">${catCount(c)}</span>`;s.onclick=()=>setCat(c);cc.appendChild(s);});
  const lc=$('#lvlChips');
  const la=document.createElement('span');la.className='chip on';la.dataset.lvl='all';la.textContent='All';la.onclick=()=>setLevel('all');lc.appendChild(la);
  C.levels.forEach(l=>{const s=document.createElement('span');s.className='chip';s.dataset.lvl=l;s.textContent=l;s.onclick=()=>setLevel(l);lc.appendChild(s);});
})();

function setCat(c){state.cat=c;document.querySelectorAll('#catChips .chip').forEach(x=>x.classList.toggle('on',x.dataset.cat===c));render();}
function setLevel(l){state.level=l;document.querySelectorAll('#lvlChips .chip').forEach(x=>x.classList.toggle('on',x.dataset.lvl===l));render();}
function setType(t,el){state.type=t;document.querySelectorAll('.type-f').forEach(x=>x.classList.toggle('on',x===el));render();}

/* render */
function match(p){
  if(state.cat!=='all'&&p.category!==state.cat)return false;
  if(state.level!=='all'&&!(p.level||[]).includes(state.level))return false;
  if(state.type!=='all'&&p.output_type!==state.type)return false;
  if(state.q){const h=(p.title+' '+p.category+' '+(p.use_case||'')+' '+(p.what_you_get||'')+' '+p.prompt+' '+(p.variables||[]).join(' ')).toLowerCase();
    return state.q.split(/\s+/).every(w=>h.includes(w));}
  return true;
}
const grid=$('#grid');
function render(){
  const items=P.filter(match);
  $('#shown').textContent=items.length+' / '+P.length+' shown';
  grid.innerHTML='';
  if(!items.length){grid.innerHTML='<div class="empty">No prompts match. Try another word or category.</div>';return;}
  const fr=document.createDocumentFragment();
  items.forEach((p,idx)=>{
    const card=document.createElement('article');card.className='glass card';
    const vars=(p.variables||[]).slice(0,6).map(v=>`<span class="var">${esc(v)}</span>`).join('');
    const lvls=(p.level||[]).map(l=>`<span class="lv">${esc(l)}</span>`).join('');
    const dot=p.output_type==='image'?'<span class="dot image" title="Generates an image"></span>':'<span class="dot text" title="Text answer"></span>';
    card.innerHTML=
      `<div class="meta">${dot}<span class="pill cat">${C.catMeta[p.category]?C.catMeta[p.category][0]+' ':''}${esc(p.category)}</span><span class="pill sign">✍️ auto-signed</span></div>`+
      `<h3>${esc(p.title)}</h3>`+
      (p.what_you_get?`<p class="yg"><b>You get:</b> ${esc(p.what_you_get)}</p>`:'')+
      (vars?`<div class="vars">${vars}</div>`:'')+
      (lvls?`<div class="lvls">${lvls}</div>`:'')+
      `<div class="cardbar"><button class="copy">📋 Copy prompt</button><button class="view">View</button></div>`;
    const cp=card.querySelector('.copy');
    cp.onclick=()=>{copyText(p.prompt);cp.classList.add('done');cp.textContent='✓ Copied!';toast('Prompt copied — paste it into your AI');setTimeout(()=>{cp.classList.remove('done');cp.textContent='📋 Copy prompt';},1600);};
    card.querySelector('.view').onclick=()=>openModal(p);
    if(idx<9){card.classList.add('reveal');card.style.animationDelay=(idx*0.03)+'s';}
    fr.appendChild(card);
  });
  grid.appendChild(fr);
}

/* modal */
const modal=$('#modal');
function openModal(p){
  const vars=(p.variables||[]).map(v=>`<span class="var">${esc(v)}</span>`).join(' ');
  const lvls=(p.level||[]).map(l=>`<span class="lv">${esc(l)}</span>`).join(' ');
  const dot=p.output_type==='image'?'<span class="dot image"></span> Image':'<span class="dot text"></span> Text';
  $('#sheet').innerHTML=
    `<button class="iconbtn x" onclick="closeModal()" aria-label="Close">✕</button>`+
    `<div class="meta"><span class="pill cat">${esc(p.category)}</span><span class="pill">${dot}</span><span class="pill sign">✍️ auto-signed</span></div>`+
    `<h3>${esc(p.title)}</h3>`+
    (p.what_you_get?`<p class="yg"><b>You get:</b> ${esc(p.what_you_get)}</p>`:'')+
    (lvls?`<div class="label">Best for</div><div class="lvls">${lvls}</div>`:'')+
    (vars?`<div class="label">Fill in these</div><div class="vars">${vars}</div>`:'')+
    `<div class="label">The prompt</div><pre class="full">${esc(p.prompt)}</pre>`+
    `<button class="copy" style="width:100%" id="mcopy">📋 Copy this prompt</button>`;
  $('#mcopy').onclick=()=>{copyText(p.prompt);toast('Prompt copied — paste it into your AI');const b=$('#mcopy');b.classList.add('done');b.textContent='✓ Copied!';setTimeout(()=>{b.classList.remove('done');b.textContent='📋 Copy this prompt';},1600);};
  modal.classList.add('open');document.body.style.overflow='hidden';
}
function closeModal(){modal.classList.remove('open');document.body.style.overflow='';}
modal.onclick=e=>{if(e.target===modal)closeModal();};
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

/* search */
let qt;$('#q').addEventListener('input',e=>{clearTimeout(qt);qt=setTimeout(()=>{state.q=e.target.value.trim().toLowerCase();render();},110);});

render();
</script>
</body>
</html>
"""

out = (TEMPLATE
    .replace("__BRAND__", esc(BRAND))
    .replace("__AUTHOR__", esc(AUTHOR))
    .replace("__ROLE__", esc(ROLE))
    .replace("__TAGLINE__", esc(TAGLINE))
    .replace("__BUILD__", BUILD)
    .replace("__COUNT__", str(COUNT))
    .replace("__NCATS__", str(len(used_cats)))
    .replace("__DATA__", jsemb(prompts))
    .replace("__CFG__", jsemb(CONFIG))
)
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)

# ---------------- prompt-pack.md ----------------
md = [f"# {BRAND}", "", f"_{COUNT} copy-paste AI prompts for teachers — curated by {AUTHOR} ({ROLE}). Built {BUILD}._", "",
      "Works with ChatGPT, Claude or Gemini. Open a prompt, replace the `[BRACKETS]`, paste it in. "
      "Every prompt instructs the AI to sign its answer so students can reach the teacher.", ""]
by_cat = {}
for p in prompts: by_cat.setdefault(p["category"], []).append(p)
for cat in used_cats:
    items = by_cat.get(cat, [])
    md.append(f"\n## {CAT_META[cat][0]} {cat}  ({len(items)})\n")
    for p in items:
        md.append(f"### {p['title']}")
        if p.get("what_you_get"): md.append(f"*You get: {p['what_you_get']}*")
        if p.get("variables"): md.append("Fill in: " + ", ".join(f"`{v}`" for v in p["variables"]))
        md.append("\n```\n" + p["prompt"].strip() + "\n```\n")
open(os.path.join(HERE, "prompt-pack.md"), "w", encoding="utf-8").write("\n".join(md))

# ---------------- WHATSAPP-MESSAGES.txt ----------------
wt = ["="*60, f"  {BRAND} — WhatsApp messages (copy & paste)", "="*60, ""]
for k, v in WA.items(): wt += [f"\n----- {k} -----\n", v, ""]
wt += ["\nContacts embedded in every prompt's signature:",
       f"  Email: {CONTACT['email']}", f"  WhatsApp: wa.me/{CONTACT['wa_num']}", f"  Instagram: @{CONTACT['insta']}"]
open(os.path.join(HERE, "WHATSAPP-MESSAGES.txt"), "w", encoding="utf-8").write("\n".join(wt))

print(f"Built index.html ({os.path.getsize(os.path.join(HERE,'index.html'))//1024} KB) · {COUNT} prompts · {len(used_cats)} categories")
