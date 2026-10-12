#!/usr/bin/env python3
"""Patch warehouse pages: dark/light theme + settings + nav reorder/decorate."""
import re, sys, os

SITE = '/home/user/site'
PAGES = ['index.html', 'campanha.html', 'lojas.html', 'franchise.html']

THEME_CSS = """
    <!-- ===== EliteDigital theme (claro/escuro) + nav decor — injetado ===== -->
    <style>
      :root{
        --ed-bg:#ffffff; --ed-bg2:#f8f9fa; --ed-card:#ffffff;
        --ed-text:#1f2937; --ed-muted:#6b7280; --ed-border:#e5e7eb;
        --ed-red:#dd3333; --ed-red-h:#b91c1c; --ed-green:#16a34a;
      }
      html[data-theme="dark"]{
        --ed-bg:#0f172a; --ed-bg2:#1e293b; --ed-card:#1e293b;
        --ed-text:#f8fafc; --ed-muted:#94a3b8; --ed-border:#334155;
      }
      body{transition:background-color .3s ease,color .3s ease;}
      /* ---------- dark overrides ---------- */
      html[data-theme="dark"] body,
      html[data-theme="dark"] #main-page-content{background:var(--ed-bg)!important;color:var(--ed-text)!important;}
      html[data-theme="dark"] #header,
      html[data-theme="dark"] .header-nav,
      html[data-theme="dark"] .header-top,
      html[data-theme="dark"] #desktop-header,
      html[data-theme="dark"] .sticky-desktop-wrapper,
      html[data-theme="dark"] #mobile-header,
      html[data-theme="dark"] .mobile-main-bar{background:#0f172a!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .header-nav a,
      html[data-theme="dark"] .header-top a{color:var(--ed-text)!important;}
      html[data-theme="dark"] .iqitmegamenu-wrapper,
      html[data-theme="dark"] .cbp-hrsub-wrapper,
      html[data-theme="dark"] .cbp-hrsub,
      html[data-theme="dark"] .cbp-menu-column-inner,
      html[data-theme="dark"] .dropdown-menu,
      html[data-theme="dark"] .dropdown-menu-custom{background:#1e293b!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .cbp-hrmenu a,
      html[data-theme="dark"] .cbp-links a,
      html[data-theme="dark"] .cbp-category-link-w a{color:var(--ed-text)!important;}
      html[data-theme="dark"] #wrapper,
      html[data-theme="dark"] #inner-wrapper,
      html[data-theme="dark"] #content-wrapper,
      html[data-theme="dark"] #main,
      html[data-theme="dark"] #left-column,
      html[data-theme="dark"] .page-content,
      html[data-theme="dark"] .card,
      html[data-theme="dark"] .facet,
      html[data-theme="dark"] .block-categories,
      html[data-theme="dark"] .cms-box{background:var(--ed-bg)!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .product-miniature,
      html[data-theme="dark"] .js-product-miniature{background:var(--ed-card)!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .product-title a,
      html[data-theme="dark"] .product-category-name,
      html[data-theme="dark"] .product-reference a,
      html[data-theme="dark"] .product-description-short a,
      html[data-theme="dark"] h1, html[data-theme="dark"] h2,
      html[data-theme="dark"] h3, html[data-theme="dark"] h4{color:var(--ed-text)!important;}
      html[data-theme="dark"] .text-muted{color:var(--ed-muted)!important;}
      html[data-theme="dark"] .form-control,
      html[data-theme="dark"] input[type="text"],
      html[data-theme="dark"] input[type="search"],
      html[data-theme="dark"] input[type="email"],
      html[data-theme="dark"] select,
      html[data-theme="dark"] textarea{background:#0f172a!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .modal-content{background:var(--ed-card)!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] .table,
      html[data-theme="dark"] .table td,
      html[data-theme="dark"] .table th{background:var(--ed-card)!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] #footer,
      html[data-theme="dark"] .footer-container,
      html[data-theme="dark"] #footer-container-first,
      html[data-theme="dark"] #footer-container-main{background:#0b1220!important;color:var(--ed-text)!important;border-color:var(--ed-border)!important;}
      html[data-theme="dark"] #footer a{color:var(--ed-muted)!important;}
      html[data-theme="dark"] .btn-secondary,
      html[data-theme="dark"] .btn-outline-secondary{background:#334155!important;border-color:#475569!important;color:#f8fafc!important;}
      html[data-theme="dark"] .breadcrumb{background:#1e293b!important;}
      html[data-theme="dark"] .breadcrumb a{color:var(--ed-text)!important;}
      html[data-theme="dark"] .page-item .page-link{background:#1e293b!important;border-color:var(--ed-border)!important;color:var(--ed-text)!important;}
      html[data-theme="dark"] .close{color:var(--ed-text)!important;}
      html[data-theme="dark"] hr{border-color:var(--ed-border)!important;}
      /* thumbnails keep white so product photos look right */
      html[data-theme="dark"] .thumbnail-container{background:#ffffff;border-radius:8px;}
      /* ---------- settings button ---------- */
      .right-nav{display:flex!important;align-items:center;justify-content:flex-end;gap:12px;}
      .ed-settings-btn{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;
        background:var(--ed-bg2);border:1px solid var(--ed-border);color:var(--ed-text);
        cursor:pointer;font-weight:600;font-size:13px;font-family:inherit;transition:all .2s ease;white-space:nowrap;}
      .ed-settings-btn:hover{background:var(--ed-red);color:#fff;border-color:var(--ed-red);}
      /* ---------- nav pills (new tabs, right side) ---------- */
      nav#cbp-hrmenu > ul{display:flex!important;align-items:center;flex-wrap:wrap;width:100%;}
      .ed-tab-ico{margin-right:6px;opacity:.8;}
      #cbp-hrmenu .nav-link.ed-nav-red{background:linear-gradient(135deg,#ff1a1a 0%,#b30000 100%)!important;color:#fff!important;
        border:1px solid #b30000!important;border-radius:8px!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;box-shadow:0 2px 8px rgba(221,51,51,.4);transition:all .2s ease;}
      #cbp-hrmenu .nav-link.ed-nav-red:hover{transform:translateY(-1px);box-shadow:0 4px 14px rgba(221,51,51,.6);color:#fff!important;}
      #cbp-hrmenu .nav-link.ed-nav-green{color:var(--ed-green)!important;font-weight:700!important;
        display:inline-flex!important;align-items:center;gap:7px;border:1px solid var(--ed-green)!important;border-radius:8px!important;
        background:rgba(22,163,74,.08)!important;transition:all .2s ease;}
      #cbp-hrmenu .nav-link.ed-nav-green:hover{background:var(--ed-green)!important;color:#fff!important;}
      .ed-nav-badge{background:#fff;color:#b30000;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:800;letter-spacing:.4px;}
      .ed-nav-badge.green{background:var(--ed-green);color:#fff;}
      #cbp-hrmenu .nav-link.ed-nav-green:hover .ed-nav-badge.green{background:#fff;color:var(--ed-green);}
      /* ---------- settings modal ---------- */
      #edSettingsModal{display:none;position:fixed;z-index:99999;left:0;top:0;width:100%;height:100%;
        background-color:rgba(0,0,0,.6);backdrop-filter:blur(4px);}
      .ed-modal-content{background-color:var(--ed-card);color:var(--ed-text);margin:10% auto;padding:24px;
        border:1px solid var(--ed-border);width:90%;max-width:480px;border-radius:16px;
        box-shadow:0 20px 25px -5px rgba(0,0,0,.3);animation:edFadeIn .25s ease-out;}
      @keyframes edFadeIn{from{opacity:0;transform:translateY(-20px)}to{opacity:1;transform:translateY(0)}}
      .ed-modal-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}
      .ed-modal-head h4{margin:0;font-size:17px;color:var(--ed-text);}
      .ed-modal-head h4 i{color:var(--ed-red);margin-right:8px;}
      .ed-modal-close{background:transparent;border:0;font-size:24px;cursor:pointer;color:var(--ed-muted);line-height:1;}
      .ed-modal-close:hover{color:var(--ed-red);}
      .ed-modal-hr{border:0;border-top:1px solid var(--ed-border);margin:12px 0;}
      .ed-theme-opts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0;}
      .ed-theme-card{border:2px solid var(--ed-border);border-radius:12px;padding:16px;text-align:center;cursor:pointer;transition:all .2s ease;color:var(--ed-text);}
      .ed-theme-card.active{border-color:var(--ed-red);background-color:rgba(221,51,51,.08);}
      .ed-theme-card i{font-size:28px;margin-bottom:8px;display:block;}
      .ed-modal-btns{text-align:right;margin-top:16px;display:flex;gap:8px;justify-content:flex-end;}
      .ed-btn-sec{background:var(--ed-bg2);border:1px solid var(--ed-border);color:var(--ed-text);border-radius:8px;padding:9px 20px;font-weight:700;cursor:pointer;font-size:13px;font-family:inherit;}
      .ed-btn-red{background:var(--ed-red);border:0;color:#fff;border-radius:8px;padding:9px 20px;font-weight:700;cursor:pointer;font-size:13px;font-family:inherit;}
      .ed-btn-red:hover{background:var(--ed-red-h);}
      @media (max-width:768px){ .ed-settings-btn span{display:none;} }
    </style>
"""

EARLY_SCRIPT = """<head><script>try{var t=localStorage.getItem('elitedigital_theme')||'light';document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>"""

MODAL_JS = """
<!-- ===== EliteDigital theme settings — injetado ===== -->
<div id="edSettingsModal">
  <div class="ed-modal-content">
    <div class="ed-modal-head">
      <h4><i class="fa fa-cog"></i>Definições de Visualização</h4>
      <button type="button" class="ed-modal-close" onclick="edToggleSettings(false)">×</button>
    </div>
    <hr class="ed-modal-hr">
    <p style="margin:0 0 4px;font-size:14px;color:var(--ed-muted);">Escolha a aparência da interface:</p>
    <div class="ed-theme-opts">
      <div class="ed-theme-card" id="ed-theme-light" onclick="edSetTheme('light')">
        <i class="fa fa-sun-o" style="color:#f59e0b;"></i>
        <strong>Modo Claro</strong>
        <small style="display:block;color:var(--ed-muted);">Fundo branco clássico</small>
      </div>
      <div class="ed-theme-card" id="ed-theme-dark" onclick="edSetTheme('dark')">
        <i class="fa fa-moon-o" style="color:#6366f1;"></i>
        <strong>Modo Escuro</strong>
        <small style="display:block;color:var(--ed-muted);">Confortável para os olhos</small>
      </div>
    </div>
    <div class="ed-modal-btns">
      <button class="ed-btn-sec" onclick="edToggleSettings(false)">Fechar</button>
      <button class="ed-btn-red" onclick="edToggleSettings(false)">Guardar</button>
    </div>
  </div>
</div>
<script>
function edToggleSettings(show){var m=document.getElementById('edSettingsModal');if(m)m.style.display=show?'block':'none';}
function edSetTheme(t){document.documentElement.setAttribute('data-theme',t);try{localStorage.setItem('elitedigital_theme',t);}catch(e){}edPaintCards(t);}
function edPaintCards(t){var l=document.getElementById('ed-theme-light'),d=document.getElementById('ed-theme-dark');if(!l||!d)return;
  if(t==='dark'){d.classList.add('active');l.classList.remove('active');}else{l.classList.add('active');d.classList.remove('active');}}
document.addEventListener('DOMContentLoaded',function(){
  var t='light';try{t=localStorage.getItem('elitedigital_theme')||'light';}catch(e){}
  document.documentElement.setAttribute('data-theme',t);edPaintCards(t);
  var m=document.getElementById('edSettingsModal');
  if(m)m.addEventListener('click',function(e){if(e.target===m)edToggleSettings(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')edToggleSettings(false);});
});
</script>
"""

SETTINGS_BTN = ('<button class="ed-settings-btn" onclick="edToggleSettings(true)" title="Definições de visualização">'
                '<i class="fa fa-cog"></i><span>Definições</span></button>')

TAB_ICONS = [
    ('NOVIDADES', 'fa-bolt'),
    ('CAMPANHAS', 'fa-tags'),
    ('LOJAS', 'fa-map-marker'),
    ('FRANCHISING', 'fa-handshake-o'),
]

def build_li(li_id, li_class, href, link_class, badge, badge_cls, icon, title, extra_li=''):
    return (f'<li id="{li_id}" class="{li_class}"{extra_li}>'
            f'<a href="{href}" class="nav-link {link_class}">'
            f'<span class="ed-nav-badge{badge_cls}">{badge}</span>'
            f'<i class="fa {icon}"></i> <span class="cbp-tab-title">{title}</span>'
            f'</a></li>')


def patch_nav(html):
    m = re.search(r'(<nav id="cbp-hrmenu".*?</nav>)', html, re.S)
    if not m:
        return html, 'NO-NAV'
    nav = m.group(1)
    # extract constructor + refurb li blocks
    mc = re.search(r'<li id="cbp-hrmenu-tab-constructor".*?</li>', nav, re.S)
    mr = re.search(r'<li id="cbp-hrmenu-tab-refurb".*?</li>', nav, re.S)
    if not mc or not mr:
        return html, 'NO-LIS'
    nav2 = nav.replace(mc.group(0), '').replace(mr.group(0), '')
    # decorate standard tabs with icons
    for title, icon in TAB_ICONS:
        nav2 = re.sub(r'(<span class="cbp-tab-title">\s*' + title + r')',
                      f'<i class="fa {icon} ed-tab-ico"></i>\\1', nav2)
    # new right-side pills
    li_c = build_li('cbp-hrmenu-tab-constructor', 'cbp-hrmenu-tab', 'construtor.html',
                    'ed-nav-red', 'NOVO', '', 'fa-cogs', 'CONSTRUTOR DE PC', ' style="margin-left:auto;"')
    li_r = build_li('cbp-hrmenu-tab-refurb', 'cbp-hrmenu-tab cbp-hrmenu-tab-refurb', 'recondicionados.html',
                    'ed-nav-green', 'PROMO', ' green', 'fa-recycle', 'RECONDICIONADOS')
    # insert before closing </ul> of this nav
    idx = nav2.rfind('</ul>')
    nav2 = nav2[:idx] + '\n\t\t\t\t\t\t' + li_c + '\n\t\t\t\t\t\t' + li_r + '\n' + nav2[idx:]
    return html.replace(nav, nav2), 'OK'


def patch_page(fname):
    p = os.path.join(SITE, fname)
    html = open(p, encoding='utf-8', errors='ignore').read()
    notes = []
    # 1. <html lang="pt"> -> data-theme
    if 'data-theme' not in html.split('<head>')[0]:
        html = html.replace('<html lang="pt">', '<html lang="pt" data-theme="light">', 1)
        notes.append('html-tag')
    # 2. early script
    if 'elitedigital_theme' not in html.split('</head>')[0]:
        html = html.replace('<head>', EARLY_SCRIPT, 1)
        notes.append('early-js')
    # 3. theme css
    if 'edSettingsModal' not in html:
        html = html.replace('</head>', THEME_CSS + '\n    </head>', 1)
        notes.append('css')
    # 4. nav
    html, navstat = patch_nav(html)
    notes.append('nav:' + navstat)
    # 5. settings button in right-nav
    if 'ed-settings-btn' not in html or html.count('ed-settings-btn') < 2:
        # insert right after right-nav opening div
        m = re.search(r'(<div class="col col-auto col-md right-nav text-right">)', html)
        if m:
            html = html.replace(m.group(1), m.group(1) + '\n' + SETTINGS_BTN, 1)
            notes.append('btn')
        else:
            notes.append('btn:NOT-FOUND')
    # 6. modal + js before </body>
    if 'id="edSettingsModal"' not in html:
        html = html.replace('</body>', MODAL_JS + '\n</body>', 1)
        notes.append('modal')
    open(p, 'w', encoding='utf-8').write(html)
    return notes


for f in PAGES:
    print(f, patch_page(f))
