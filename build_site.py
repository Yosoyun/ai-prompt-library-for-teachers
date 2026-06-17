#!/usr/bin/env python3
"""Build a self-contained index.html + prompt-pack.md from data/prompts.json.
Run:  python3 build_site.py
"""
import json, html, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
prompts = json.load(open(os.path.join(HERE, "data", "prompts.json"), encoding="utf-8"))

AUTHOR = "Indrajeet Yadav"
TITLE = "AI Prompt Library for Teachers"
COUNT = len(prompts)

CATEGORY_ORDER = [
    "Solutions & Worked Examples", "Practice, DPP & Tests", "Question Papers & Assessment",
    "Concepts, Proofs & Theory", "Doubt-Solving & Remedial", "Visual & Diagram Maths",
    "Lesson Planning & Notes", "Student Feedback & Mentoring", "WhatsApp & Parent Communication",
    "Content & Social Media", "AI Productivity & Workflow", "Prompt-Writing & Meta",
]
CAT_EMOJI = {
    "Solutions & Worked Examples": "✍️", "Practice, DPP & Tests": "📝",
    "Question Papers & Assessment": "📄", "Concepts, Proofs & Theory": "📐",
    "Doubt-Solving & Remedial": "🔧", "Visual & Diagram Maths": "📊",
    "Lesson Planning & Notes": "🗂️", "Student Feedback & Mentoring": "🧑‍🏫",
    "WhatsApp & Parent Communication": "💬", "Content & Social Media": "🎬",
    "AI Productivity & Workflow": "⚡", "Prompt-Writing & Meta": "🧩",
}

# ---------- WhatsApp ready-to-paste messages (single source of truth) ----------
WA = {
"Invite (English)": """🎓 *AI Prompt Library for Teachers*

219 ready-to-use prompts that save hours every day — solutions, DPPs, question papers, doubt-solving, lesson plans, parent & WhatsApp messages, YouTube/Insta content and more.

✅ 100% copy-paste. Works on ChatGPT, Claude or Gemini (free versions too).
🧩 Open it → pick a prompt → fill the [BLANKS] → paste into the AI.

👉 Open here: [PASTE YOUR LINK]

Made for faculty, by Indrajeet Yadav.""",

"How to use daily (English)": """📌 *How to use the Prompt Library every day*

1️⃣ Open the link and bookmark it on your phone.
2️⃣ Use the 🔍 search box, or tap a category (DPP, Question Paper, Doubt-Solving…).
3️⃣ Tap *Copy* on any prompt.
4️⃣ Paste it into ChatGPT / Claude / Gemini.
5️⃣ Replace the words in [BRACKETS] with your details — e.g. [TOPIC] → Integration, [GRADE] → Class 12.
6️⃣ Send. Edit the result and use it in class.

💡 *Daily ideas:*
• Morning — generate today's DPP / warm-up questions.
• Before class — make a quick lesson plan or board-work plan.
• Doubt time — paste a student's question for a step-by-step solution.
• Evening — turn your lesson into a WhatsApp note or a YouTube/Insta post.

Start with just *one* prompt a day. 🚀""",

"Invite (Hindi)": """🎓 *शिक्षकों के लिए AI प्रॉम्प्ट लाइब्रेरी*

रोज़ घंटों बचाने वाले 219 तैयार प्रॉम्प्ट — हल, DPP, प्रश्न-पत्र, डाउट सॉल्विंग, लेसन प्लान, पैरेंट/WhatsApp मैसेज, YouTube/Insta कंटेंट और भी बहुत कुछ।

✅ पूरी तरह कॉपी-पेस्ट। ChatGPT, Claude या Gemini (फ्री वर्ज़न भी) पर चलता है।
🧩 खोलें → प्रॉम्प्ट चुनें → [BRACKETS] भरें → AI में पेस्ट करें।

👉 यहाँ खोलें: [अपना लिंक पेस्ट करें]

शिक्षकों के लिए — Indrajeet Yadav द्वारा।""",
}

# Live hosted link — inserted into every WhatsApp message
LIVE_URL = "https://yosoyun.github.io/ai-prompt-library-for-teachers/"
for _k in WA:
    WA[_k] = WA[_k].replace("[PASTE YOUR LINK]", LIVE_URL).replace("[अपना लिंक पेस्ट करें]", LIVE_URL)

# ---------- helpers ----------
def esc(s): return html.escape(s or "", quote=True)

# stable category counts
counts = {c: 0 for c in CATEGORY_ORDER}
for p in prompts:
    counts[p["category"]] = counts.get(p["category"], 0) + 1

# embed data safely
data_json = json.dumps(prompts, ensure_ascii=False).replace("</", "<\\/")
wa_json = json.dumps(WA, ensure_ascii=False).replace("</", "<\\/")

build_date = datetime.date.today().isoformat()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="__COUNT__ ready-to-use, copy-paste AI prompts for mathematics and school faculty. Works with ChatGPT, Claude and Gemini."/>
<title>__TITLE__</title>
<style>
:root{
  --bg:#0f1226; --bg2:#151935; --card:#ffffff; --ink:#1a1c2e; --muted:#5b6072;
  --line:#e7e8f0; --accent:#5b54ff; --accent2:#8b5cf6; --accent-soft:#eef0ff;
  --ok:#16a34a; --chip:#f2f3f9; --shadow:0 1px 2px rgba(20,22,50,.06),0 8px 24px rgba(20,22,50,.06);
  --radius:16px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;
  color:var(--ink);background:#f6f7fb;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px}

/* hero */
.hero{background:radial-gradient(1200px 400px at 10% -20%,#3a2fb0 0%,transparent 60%),
  radial-gradient(900px 380px at 95% 0%,#7c3aed 0%,transparent 55%),linear-gradient(160deg,#0f1226,#1b1f44);
  color:#fff;padding:46px 0 34px}
.hero h1{margin:0 0 8px;font-size:30px;letter-spacing:-.5px;font-weight:800}
.hero p{margin:0;color:#c9cdf0;max-width:680px;font-size:15.5px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.badge{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);color:#fff;
  padding:6px 12px;border-radius:999px;font-size:13px;font-weight:600;backdrop-filter:blur(4px)}
.kicker{font-size:12.5px;letter-spacing:2px;text-transform:uppercase;color:#a9aef0;font-weight:700;margin-bottom:10px}

/* how-to + whatsapp */
.panel{background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);
  padding:20px 20px 8px;margin-top:-22px;position:relative;z-index:3}
.panel h2{margin:2px 0 4px;font-size:18px}
.panel .sub{color:var(--muted);font-size:14px;margin:0 0 14px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 16px}
.step{background:var(--accent-soft);border:1px solid #e3e5ff;border-radius:12px;padding:11px 12px;font-size:13.5px}
.step b{display:block;color:var(--accent);font-size:12px;margin-bottom:3px}
.wa-row{display:flex;flex-wrap:wrap;gap:10px;border-top:1px dashed var(--line);padding:14px 0 16px;align-items:center}
.wa-row .label{font-weight:700;font-size:13.5px;margin-right:4px}
.wa-btn{display:inline-flex;align-items:center;gap:7px;background:#25d366;color:#04391c;border:none;
  font-weight:700;font-size:13px;padding:9px 14px;border-radius:10px;cursor:pointer;transition:.15s}
.wa-btn:hover{filter:brightness(.97);transform:translateY(-1px)}
.wa-btn.alt{background:#eef0ff;color:var(--accent)}

/* controls */
.controls{position:sticky;top:0;z-index:20;background:#f6f7fbe6;backdrop-filter:blur(8px);
  padding:14px 0 8px;margin-top:18px;border-bottom:1px solid var(--line)}
.search{display:flex;gap:10px;align-items:center}
.search input{flex:1;font-size:15px;padding:13px 14px 13px 42px;border:1px solid var(--line);border-radius:12px;
  background:#fff url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%235b6072' stroke-width='2'><circle cx='11' cy='11' r='7'/><path d='M21 21l-4-4'/></svg>") 14px center no-repeat;
  box-shadow:var(--shadow);outline:none}
.search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.count{font-size:13px;color:var(--muted);white-space:nowrap;font-weight:600}
.chips{display:flex;gap:8px;overflow-x:auto;padding:12px 0 4px;scrollbar-width:thin}
.chip{white-space:nowrap;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:13px;
  font-weight:600;padding:8px 13px;border-radius:999px;cursor:pointer;transition:.12s}
.chip:hover{border-color:var(--accent)}
.chip.active{background:var(--accent);border-color:var(--accent);color:#fff}
.chip .n{opacity:.6;font-weight:700;margin-left:5px}
.chip.active .n{opacity:.9}

/* cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:22px 0 60px;align-items:start}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);
  display:flex;flex-direction:column;overflow:hidden}
.card .top{padding:15px 16px 0}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:9px}
.tag{font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;background:var(--chip);color:var(--muted)}
.tag.cat{background:var(--accent-soft);color:var(--accent)}
.card h3{margin:0 0 5px;font-size:16px;line-height:1.3}
.usecase{color:var(--muted);font-size:13.5px;margin:0 0 11px}
.vars{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 6px}
.var{font-size:11px;font-family:ui-monospace,Menlo,monospace;background:#fff7ed;color:#b45309;
  border:1px solid #fde7c8;padding:2px 7px;border-radius:6px}
.promptbox{position:relative;margin:8px 16px 0;border-top:1px solid var(--line)}
pre.prompt{white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:12.5px;line-height:1.55;color:#2b2e44;background:#fbfbfe;border:1px solid var(--line);border-radius:12px;
  padding:13px 14px;margin:12px 0 0;max-height:188px;overflow:hidden;position:relative;flex:0 0 auto}
pre.prompt.open{max-height:none}
.fade{position:absolute;left:0;right:0;bottom:0;height:54px;border-radius:0 0 12px 12px;
  background:linear-gradient(transparent,#fbfbfe);pointer-events:none;display:none}
.cardbar{display:flex;gap:8px;padding:12px 16px 16px;align-items:center}
.copy{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--accent);
  color:#fff;border:none;font-weight:700;font-size:13.5px;padding:11px;border-radius:10px;cursor:pointer;transition:.15s}
.copy:hover{filter:brightness(1.05);transform:translateY(-1px)}
.copy.copied{background:var(--ok)}
.toggle{background:#fff;border:1px solid var(--line);color:var(--muted);font-weight:600;font-size:12.5px;
  padding:11px 13px;border-radius:10px;cursor:pointer}
.toggle:hover{border-color:var(--accent);color:var(--accent)}
.empty{text-align:center;color:var(--muted);padding:60px 0;font-size:15px}

footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--muted);font-size:13px;text-align:center}
footer b{color:var(--ink)}

/* toast */
#toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);opacity:0;
  background:#111327;color:#fff;padding:11px 18px;border-radius:10px;font-size:13.5px;font-weight:600;
  box-shadow:0 10px 30px rgba(0,0,0,.25);transition:.2s;z-index:50;pointer-events:none}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

@media (max-width:620px){
  .hero h1{font-size:24px}.grid{grid-template-columns:1fr}
  .panel{margin-top:-16px}
}
</style>
</head>
<body>

<header class="hero">
  <div class="wrap">
    <div class="kicker">For Faculty · ChatGPT · Claude · Gemini</div>
    <h1>__TITLE__</h1>
    <p>__COUNT__ ready-to-use, copy-paste prompts for everyday teaching — solutions, DPPs, question papers,
       doubt-solving, lesson plans, parent messages and content. No tech skills needed.</p>
    <div class="badges">
      <span class="badge">__COUNT__ prompts</span>
      <span class="badge">12 categories</span>
      <span class="badge">100% copy-paste</span>
      <span class="badge">Works offline</span>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="panel">
    <h2>How to use it — daily</h2>
    <p class="sub">Open · pick a prompt · fill the <code>[BLANKS]</code> · paste into any AI chatbot.</p>
    <div class="steps">
      <div class="step"><b>STEP 1</b>Tap a category or search.</div>
      <div class="step"><b>STEP 2</b>Press <b>Copy</b> on a prompt.</div>
      <div class="step"><b>STEP 3</b>Paste into ChatGPT / Claude / Gemini.</div>
      <div class="step"><b>STEP 4</b>Replace [TOPIC], [GRADE]…</div>
      <div class="step"><b>STEP 5</b>Send & use the result in class.</div>
    </div>
    <div class="wa-row" id="wa-row">
      <span class="label">📲 Share with teachers:</span>
      <!-- buttons injected -->
    </div>
  </section>

  <section class="controls">
    <div class="wrap" style="padding:0">
      <div class="search">
        <input id="q" type="search" placeholder="Search 219 prompts — e.g. DPP, integration, doubt, question paper, WhatsApp…" autocomplete="off"/>
        <span class="count" id="count"></span>
      </div>
      <div class="chips" id="chips"></div>
    </div>
  </section>

  <section class="grid" id="grid"></section>
</main>

<footer>
  <div class="wrap">
    <b>__TITLE__</b> · __COUNT__ curated prompts · Built __DATE__<br/>
    Created &amp; curated by <b>__AUTHOR__</b>. Free to share with fellow teachers — please keep this credit.
  </div>
</footer>

<div id="toast">Copied!</div>

<script id="prompt-data" type="application/json">__DATA__</script>
<script id="wa-data" type="application/json">__WA__</script>
<script>
const PROMPTS = JSON.parse(document.getElementById('prompt-data').textContent);
const WA = JSON.parse(document.getElementById('wa-data').textContent);
const CAT_ORDER = __CATORDER__;
const CAT_EMOJI = __CATEMOJI__;
const grid = document.getElementById('grid');
const chipsEl = document.getElementById('chips');
const qEl = document.getElementById('q');
const countEl = document.getElementById('count');
let activeCat = 'All', query = '';

/* ---- clipboard with file:// fallback ---- */
function copyText(text){
  if(navigator.clipboard && window.isSecureContext){
    return navigator.clipboard.writeText(text).catch(()=>fallbackCopy(text));
  }
  return Promise.resolve(fallbackCopy(text));
}
function fallbackCopy(text){
  const ta=document.createElement('textarea');
  ta.value=text; ta.style.position='fixed'; ta.style.top='-9999px';
  document.body.appendChild(ta); ta.focus(); ta.select();
  try{document.execCommand('copy');}catch(e){}
  document.body.removeChild(ta);
}
let toastT;
function toast(msg){
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  clearTimeout(toastT); toastT=setTimeout(()=>t.classList.remove('show'),1400);
}

/* ---- WhatsApp share buttons ---- */
(function(){
  const row=document.getElementById('wa-row');
  Object.keys(WA).forEach((k,i)=>{
    const b=document.createElement('button');
    b.className='wa-btn'+(i>0?' alt':'');
    b.innerHTML=(i===0?'💬 ':'📋 ')+'Copy: '+k;
    b.onclick=()=>{copyText(WA[k]);toast('WhatsApp message copied — paste it into your group');};
    row.appendChild(b);
  });
})();

/* ---- chips ---- */
function buildChips(){
  const cats=['All',...CAT_ORDER];
  cats.forEach(c=>{
    const n = c==='All'?PROMPTS.length:PROMPTS.filter(p=>p.category===c).length;
    if(c!=='All' && n===0) return;
    const b=document.createElement('button');
    b.className='chip'+(c===activeCat?' active':'');
    b.innerHTML=(c==='All'?'★ All':((CAT_EMOJI[c]||'')+' '+c))+' <span class="n">'+n+'</span>';
    b.onclick=()=>{activeCat=c;document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};
    chipsEl.appendChild(b);
  });
}

/* ---- render ---- */
function matches(p){
  if(activeCat!=='All' && p.category!==activeCat) return false;
  if(!query) return true;
  const hay=(p.title+' '+p.category+' '+(p.use_case||'')+' '+p.prompt+' '+(p.variables||[]).join(' ')).toLowerCase();
  return query.split(/\s+/).every(w=>hay.includes(w));
}
function render(){
  const items=PROMPTS.filter(matches);
  countEl.textContent=items.length+' / '+PROMPTS.length+' shown';
  grid.innerHTML='';
  if(!items.length){grid.innerHTML='<div class="empty">No prompts match. Try another word or category.</div>';return;}
  const frag=document.createDocumentFragment();
  items.forEach(p=>{
    const card=document.createElement('article');card.className='card';
    const vars=(p.variables||[]).slice(0,8).map(v=>'<span class="var">'+escapeHtml(v)+'</span>').join('');
    const toolTag = p.tool && p.tool!=='Any' ? '<span class="tag">'+escapeHtml(p.tool)+'</span>' : '';
    card.innerHTML =
      '<div class="top">'+
        '<div class="tags"><span class="tag cat">'+(CAT_EMOJI[p.category]||'')+' '+escapeHtml(p.category)+'</span>'+toolTag+'</div>'+
        '<h3>'+escapeHtml(p.title)+'</h3>'+
        (p.use_case?'<p class="usecase">'+escapeHtml(p.use_case)+'</p>':'')+
        (vars?'<div class="vars">'+vars+'</div>':'')+
      '</div>'+
      '<div class="promptbox"><pre class="prompt">'+escapeHtml(p.prompt)+'</pre><div class="fade"></div></div>'+
      '<div class="cardbar">'+
        '<button class="copy">📋 Copy prompt</button>'+
        '<button class="toggle">Expand</button>'+
      '</div>';
    const pre=card.querySelector('pre.prompt');
    const tog=card.querySelector('.toggle');
    const fade=card.querySelector('.fade');
    tog.onclick=()=>{const open=pre.classList.toggle('open');tog.textContent=open?'Collapse':'Expand';
      if(open){fade.style.display='none';}else{clampCard(card);}};
    const cp=card.querySelector('.copy');
    cp.onclick=()=>{copyText(p.prompt);cp.classList.add('copied');cp.textContent='✓ Copied!';toast('Prompt copied — paste it into your AI chatbot');
      setTimeout(()=>{cp.classList.remove('copied');cp.textContent='📋 Copy prompt';},1600);};
    frag.appendChild(card);
  });
  grid.appendChild(frag);
  refreshClamps();
  requestAnimationFrame(refreshClamps);
}
function clampCard(card){
  const pre=card.querySelector('pre.prompt'),tog=card.querySelector('.toggle'),fade=card.querySelector('.fade');
  if(pre.classList.contains('open')){tog.style.display='';fade.style.display='none';return;}
  const more = pre.scrollHeight > pre.clientHeight + 4;
  tog.style.display = more ? '' : 'none';
  fade.style.display = more ? 'block' : 'none';
}
function refreshClamps(){document.querySelectorAll('.card').forEach(clampCard);}
let rcT;
window.addEventListener('resize',()=>{clearTimeout(rcT);rcT=setTimeout(refreshClamps,160);});
window.addEventListener('load',()=>requestAnimationFrame(refreshClamps));
function escapeHtml(s){return (s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

let qT;
qEl.addEventListener('input',e=>{clearTimeout(qT);qT=setTimeout(()=>{query=e.target.value.trim().toLowerCase();render();},120);});
buildChips();render();
</script>
</body>
</html>
"""

HTML = (HTML
    .replace("__TITLE__", esc(TITLE))
    .replace("__AUTHOR__", esc(AUTHOR))
    .replace("__COUNT__", str(COUNT))
    .replace("__DATE__", build_date)
    .replace("__CATORDER__", json.dumps(CATEGORY_ORDER, ensure_ascii=False))
    .replace("__CATEMOJI__", json.dumps(CAT_EMOJI, ensure_ascii=False))
    .replace("__DATA__", data_json)
    .replace("__WA__", wa_json)
)

with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)

# ---------- prompt-pack.md ----------
md = [f"# {TITLE}", "", f"_{COUNT} copy-paste AI prompts for teachers — curated by {AUTHOR}. Built {build_date}._", ""]
md.append("Works with ChatGPT, Claude or Gemini. Open a prompt, replace the `[BRACKETS]`, paste it in.\n")
by_cat = {}
for p in prompts:
    by_cat.setdefault(p["category"], []).append(p)
for cat in CATEGORY_ORDER:
    items = by_cat.get(cat, [])
    if not items: continue
    md.append(f"\n## {CAT_EMOJI.get(cat,'')} {cat}  ({len(items)})\n")
    for p in items:
        md.append(f"### {p['title']}")
        if p.get("use_case"): md.append(f"*{p['use_case']}*")
        if p.get("variables"): md.append("Fill in: " + ", ".join(f"`{v}`" for v in p["variables"]))
        md.append("\n```\n" + p["prompt"].strip() + "\n```\n")
with open(os.path.join(HERE, "prompt-pack.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# ---------- WHATSAPP-MESSAGES.txt ----------
wa_txt = ["="*60, "  WHATSAPP MESSAGES — copy & paste into your faculty groups", "="*60, ""]
for k, v in WA.items():
    wa_txt += [f"\n----- {k} -----\n", v, ""]
wa_txt += ["\nThe live link is already filled in above:",
           "  https://yosoyun.github.io/ai-prompt-library-for-teachers/",
           "Just copy a message and paste it into your WhatsApp groups."]
with open(os.path.join(HERE, "WHATSAPP-MESSAGES.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(wa_txt))

print(f"Built index.html ({os.path.getsize(os.path.join(HERE,'index.html'))//1024} KB), prompt-pack.md, WHATSAPP-MESSAGES.txt")
print(f"{COUNT} prompts across {len([c for c in CATEGORY_ORDER if by_cat.get(c)])} categories")
