import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_copy import *
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = """  :root { --ink:#1a1f1d; --head:#24302c; --accent:#1A8A8F; --muted:#667; }
  body { font-family: -apple-system, "Hiragino Sans", "PingFang TC", "Apple SD Gothic Neo", "Yu Gothic", sans-serif; line-height: 1.8; color: var(--ink); max-width: 720px; margin: 0 auto; padding: 24px; }
  .hero { background: linear-gradient(160deg,#0f4f52,#1A8A8F 55%,#23A6A6); color:#eaf7f6; border-radius: 20px; padding: 34px 26px; margin: 6px 0 20px; }
  .hero h1 { color:#fff; border:0; font-size:1.7rem; margin:0 0 6px; }
  .hero p { color:#d4efed; margin:0; }
  h1 { font-size: 1.5rem; border-bottom: 2px solid var(--head); padding-bottom: 8px; }
  h2 { font-size: 1.12rem; margin-top: 1.6em; color: var(--head); }
  h3 { font-size: 1rem; margin-top: 1.3em; }
  a { color: var(--accent); }
  .meta { color: var(--muted); font-size: 0.9rem; }
  .langnav { font-size: 0.95rem; margin: 12px 0 20px; }
  .langnav a { margin-right: 12px; }
  ul { padding-left: 1.2em; }
  hr { border: none; border-top: 1px solid #ddd; margin: 40px 0; }"""

def page(title, desc, sections):
    nav = '<div class="langnav">\n  ' + ''.join(f'<a href="#{c}">{n}</a>' for c, n in LANGS) + '\n</div>\n'
    body = '\n<hr>\n\n'.join(sections)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>
{CSS}
</style>
</head>
<body>

{nav}
{body}

</body>
</html>
"""

def lang_attr(c): return 'zh-Hant' if c == 'zh-hant' else c

idx = []
for c, n in LANGS:
    h, sub, para, sup, priv = INDEX[c]
    idx.append(f'<!-- ===================== {n} ===================== -->\n<section id="{c}" lang="{lang_attr(c)}">\n<div class="hero">\n  <h1>{h}</h1>\n  <p>{sub}</p>\n</div>\n<p>{para}</p>\n<ul>\n  <li><a href="./support.html#{c}">{sup}</a></li>\n  <li><a href="./privacy.html#{c}">{priv}</a></li>\n</ul>\n</section>')
open(f'{OUT}/index.html', 'w').write(page("QuitDays — Quit Tracker &amp; Sober Day Counter / 禁煙・禁酒カウンター / Contador para dejar de fumar / 戒菸・戒酒天數計數器 / 금연·금주 카운터",
    "QuitDays counts every day since you quit — smoking, vaping, alcohol, sugar, social media and more — with money saved, milestones and widgets.", idx))

pv = []
for c, n in LANGS:
    t, intro, items = PRIVACY[c]
    parts = [f'<!-- ===================== {n} ===================== -->\n<section id="{c}" lang="{lang_attr(c)}">\n<h1>{t}</h1>\n<p class="meta">{LAST_UPDATED_LABEL[c]}: {UPDATED[c]}</p>\n<p>{intro}</p>']
    for h2, b in items:
        parts.append(f'<h2>{h2}</h2>\n' + (b if b.startswith('<') or '<ul>' in b.split('</p>')[0][:5] else f'<p>{b}</p>' if '<ul>' not in b else b.replace('<ul>', '</p><ul>', 1).join(['<p>', '']) ))
    parts.append('</section>')
    pv.append('\n'.join(parts))
open(f'{OUT}/privacy.html', 'w').write(page("QuitDays — Privacy Policy / プライバシーポリシー / Política de privacidad / 隱私權政策 / 개인정보 처리방침",
    "Privacy policy for the iOS app QuitDays.", pv))

sp = []
for c, n in LANGS:
    t, intro, ch, note, fh, faq, rh, rintro, items = SUPPORT[c]
    qa = '\n'.join(f'<h3>Q. {q}</h3>\n<p>{a}</p>' for q, a in faq)
    li = '\n'.join(f'  <li>{i}</li>' for i in items)
    sp.append(f'<!-- ===================== {n} ===================== -->\n<section id="{c}" lang="{lang_attr(c)}">\n<h1>{t}</h1>\n<p>{intro}</p>\n<h2>{ch}</h2>\n<p>{EMAIL_LABEL[c]}: <a href="mailto:{EMAIL}">{EMAIL}</a></p>\n<p>{note}</p>\n<h2>{fh}</h2>\n{qa}\n<h2>{rh}</h2>\n<p>{rintro}</p>\n<ul>\n{li}\n</ul>\n</section>')
open(f'{OUT}/support.html', 'w').write(page("QuitDays — Support / サポート / Soporte / 支援 / 지원", "Support page for the iOS app QuitDays.", sp))
print("ok")
