#!/usr/bin/env python3
"""Round 2: red lines on the 2 new nav tabs + polished right-side buttons."""
import re, os

SITE = '/home/user/site'
WAREHOUSE = ['index.html', 'campanha.html', 'lojas.html', 'franchise.html']

# ---------- 1. warehouse CSS: pills -> red lines ----------
OLD_PILLS = """      #cbp-hrmenu .nav-link.ed-nav-red{background:linear-gradient(135deg,#ff1a1a 0%,#b30000 100%)!important;color:#fff!important;
        border:1px solid #b30000!important;border-radius:8px!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;box-shadow:0 2px 8px rgba(221,51,51,.4);transition:all .2s ease;}
      #cbp-hrmenu .nav-link.ed-nav-red:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(221,51,51,.6);color:#fff!important;}
      #cbp-hrmenu .nav-link.ed-nav-green{color:var(--ed-green)!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;border:1px solid var(--ed-green)!important;border-radius:8px!important;
        background:rgba(22,163,74,.08)!important;transition:all .2s ease;}
      #cbp-hrmenu .nav-link.ed-nav-green:hover{background:var(--ed-green)!important;color:#fff!important;}
      .ed-nav-badge{background:#fff;color:#b30000;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:800;letter-spacing:.4px;}
      .ed-nav-badge.green{background:var(--ed-green);color:#fff;}
      #cbp-hrmenu .nav-link.ed-nav-green:hover .ed-nav-badge.green{background:#fff;color:var(--ed-green);}"""

NEW_PILLS = """      #cbp-hrmenu .nav-link.ed-nav-red{background:linear-gradient(135deg,#ff1a1a 0%,#b30000 100%)!important;color:#fff!important;
        border:1px solid #ef4444!important;border-top:3px solid #fca5a5!important;border-radius:8px!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;
        box-shadow:0 2px 8px rgba(221,51,51,.4),inset 0 1px 0 rgba(255,255,255,.25);transition:all .2s ease;}
      #cbp-hrmenu .nav-link.ed-nav-red:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(221,51,51,.6);color:#fff!important;}
      #cbp-hrmenu .nav-link.ed-nav-green{color:#b91c1c!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;
        border:1px solid #dd3333!important;border-top:3px solid #dd3333!important;border-radius:8px!important;
        background:#ffffff!important;transition:all .2s ease;box-shadow:0 2px 8px rgba(221,51,51,.18);}
      #cbp-hrmenu .nav-link.ed-nav-green:hover{background:var(--ed-red)!important;color:#fff!important;
        border-color:var(--ed-red)!important;transform:translateY(-1px);box-shadow:0 4px 14px rgba(221,51,51,.5);}
      html[data-theme="dark"] #cbp-hrmenu .nav-link.ed-nav-green{background:rgba(221,51,51,.12)!important;color:#fca5a5!important;}
      html[data-theme="dark"] #cbp-hrmenu .nav-link.ed-nav-green:hover{background:var(--ed-red)!important;color:#fff!important;}
      .ed-nav-badge{background:#fff;color:#b30000;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:800;letter-spacing:.4px;}
      .ed-nav-badge.green{background:var(--ed-green);color:#fff;}
      #cbp-hrmenu .nav-link.ed-nav-green:hover .ed-nav-badge.green{background:#fff;color:var(--ed-green);}"""

# ---------- 2. warehouse CSS: right-side buttons polish ----------
OLD_BTNS = """      .ed-settings-btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;
        background:var(--ed-bg2);border:1px solid var(--ed-border);color:var(--ed-text);
        cursor:pointer;font-weight:600;font-size:13px;font-family:inherit;transition:all .2s ease;white-space:nowrap;}
      .ed-settings-btn:hover{background:var(--ed-red);color:#fff;border-color:var(--ed-red);}"""

NEW_BTNS = """      .ed-settings-btn{display:inline-flex;align-items:center;gap:7px;padding:0 15px;height:32px;border-radius:20px;
        background:var(--ed-card);border:1px solid var(--ed-border);color:var(--ed-text);
        box-shadow:0 1px 3px rgba(0,0,0,.08);cursor:pointer;font-weight:700;font-size:12.5px;letter-spacing:.2px;
        font-family:inherit;transition:all .2s ease;white-space:nowrap;}
      .ed-settings-btn i{color:var(--ed-red);font-size:14px;transition:color .2s ease,transform .3s ease;}
      .ed-settings-btn:hover{background:var(--ed-red);border-color:var(--ed-red);color:#fff;transform:translateY(-1px);box-shadow:0 3px 10px rgba(221,51,51,.35);}
      .ed-settings-btn:hover i{color:#fff;transform:rotate(40deg);}
      .ed-settings-btn:focus-visible{outline:2px solid var(--ed-red);outline-offset:2px;}
      .ed-wishlist-btn{display:inline-flex!important;align-items:center;gap:7px;padding:0 15px;height:32px;border-radius:20px;
        background:var(--ed-card)!important;border:1px solid var(--ed-border)!important;color:var(--ed-text)!important;
        font-weight:700!important;font-size:12.5px!important;text-decoration:none!important;box-shadow:0 1px 3px rgba(0,0,0,.08);
        transition:all .2s ease;white-space:nowrap;}
      .ed-wishlist-btn i{color:var(--ed-red);font-size:14px;}
      .ed-wishlist-btn:hover{background:var(--ed-red)!important;border-color:var(--ed-red)!important;color:#fff!important;
        transform:translateY(-1px);box-shadow:0 3px 10px rgba(221,51,51,.35);text-decoration:none!important;}
      .ed-wishlist-btn:hover i{color:#fff!important;}
      .ed-wishlist-btn .ed-wish-count{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;
        padding:0 5px;border-radius:12px;background:var(--ed-red);color:#fff;font-size:11px;font-weight:800;}
      .ed-wishlist-btn:hover .ed-wish-count{background:#fff;color:var(--ed-red);}
      /* main header account / cart buttons */
      #desktop-header .header-btn-w .header-btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none!important;transition:all .2s ease;}
      #desktop-header .header-btn-w .header-btn .icon{font-size:22px;transition:color .2s ease,transform .2s ease;}
      #desktop-header .header-btn-w .header-btn:hover .icon{color:var(--ed-red);transform:translateY(-1px);}
      #desktop-header .header-btn-w .header-btn:hover .title{color:var(--ed-red);}
      #desktop-header .header-btn-w .header-btn:hover{text-decoration:none!important;}"""

for fname in WAREHOUSE:
    p = os.path.join(SITE, fname)
    html = open(p, encoding='utf-8', errors='ignore').read()
    notes = []
    if OLD_PILLS in html:
        html = html.replace(OLD_PILLS, NEW_PILLS)
        notes.append('pills')
    else:
        notes.append('pills:NOT-FOUND')
    if OLD_BTNS in html:
        html = html.replace(OLD_BTNS, NEW_BTNS)
        notes.append('btns')
    else:
        notes.append('btns:NOT-FOUND')
    # wishlist anchor -> pill button + count badge (drop the parens)
    pat_a = re.compile(r'<a href="//www\.elitedigital\.pt/module/iqitwishlist/view">')
    if pat_a.search(html) and 'class="ed-wishlist-btn"' not in html:
        html = pat_a.sub('<a class="ed-wishlist-btn" href="//www.elitedigital.pt/module/iqitwishlist/view">', html, count=1)
        notes.append('wish-a')
    else:
        notes.append('wish-a:skip')
    pat_n = re.compile(r'Lista de Desejos\s*\(<span id="iqitwishlist-nb">(\d*)</span>\)')
    if pat_n.search(html):
        html = pat_n.sub(r'Lista de Desejos <span class="ed-wish-count" id="iqitwishlist-nb">\1</span>', html, count=1)
        notes.append('wish-n')
    else:
        notes.append('wish-n:NOT-FOUND')
    open(p, 'w', encoding='utf-8').write(html)
    print(fname, notes)

# ---------- 3. construtor.html: red lines on both pills (dark bar) ----------
p = os.path.join(SITE, 'construtor.html')
html = open(p, encoding='utf-8', errors='ignore').read()
old_red = "    .ed-pill-red{background:linear-gradient(135deg,#ff1a1a 0%,#b30000 100%)!important;color:#fff!important;box-shadow:0 2px 8px rgba(221,51,51,.45)}"
new_red = ("    .ed-pill-red{background:linear-gradient(135deg,#ff1a1a 0%,#b30000 100%)!important;color:#fff!important;"
           "border:1px solid #ef4444!important;border-top:3px solid #fca5a5!important;"
           "box-shadow:0 2px 8px rgba(221,51,51,.45),inset 0 1px 0 rgba(255,255,255,.25)}")
old_green = ("    .ed-pill-green{background:rgba(22,163,74,.14)!important;color:#4ade80!important;border:1px solid rgba(74,222,128,.45)}\n"
             "    .ed-pill-green:hover{background:var(--accent-green)!important;color:#fff!important;border-color:var(--accent-green)}")
new_green = ("    .ed-pill-green{background:rgba(255,255,255,.06)!important;color:#fecaca!important;"
             "border:1px solid #dd3333!important;border-top:3px solid #dd3333!important}\n"
             "    .ed-pill-green:hover{background:var(--accent-red)!important;color:#fff!important;"
             "border-color:var(--accent-red)!important;transform:translateY(-1px);box-shadow:0 4px 14px rgba(221,51,51,.5)}")
print('construtor pills:', old_red in html, old_green in html)
html = html.replace(old_red, new_red).replace(old_green, new_green)
open(p, 'w', encoding='utf-8').write(html)

# ---------- 4. recondicionados.html: red lines on constructor pill + red top line on refurb tab ----------
p = os.path.join(SITE, 'recondicionados.html')
html = open(p, encoding='utf-8', errors='ignore').read()
old_c = (".main-nav a.nav-constructor {\n      background: linear-gradient(135deg, #ff1a1a 0%, #b30000 100%);\n"
         "      color: #fff;\n      box-shadow: 0 2px 8px rgba(221, 51, 51, 0.4);\n    }")
new_c = (".main-nav a.nav-constructor {\n      background: linear-gradient(135deg, #ff1a1a 0%, #b30000 100%);\n"
         "      color: #fff;\n      border: 1px solid #ef4444;\n      border-top: 3px solid #fca5a5;\n"
         "      box-shadow: 0 2px 8px rgba(221, 51, 51, 0.4), inset 0 1px 0 rgba(255,255,255,.25);\n    }")
old_r = "    .main-nav a.nav-refurb { box-shadow: 0 2px 8px rgba(22,163,74,.4); }"
new_r = "    .main-nav a.nav-refurb { box-shadow: 0 2px 8px rgba(22,163,74,.4); border: 1px solid #dd3333; border-top: 3px solid #dd3333; }"
print('recondicionados pills:', old_c in html, old_r in html)
html = html.replace(old_c, new_c).replace(old_r, new_r)
open(p, 'w', encoding='utf-8').write(html)
print('done')
