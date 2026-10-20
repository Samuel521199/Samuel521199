"""Build self-contained profile SVG typography and technical diagrams.
Run: python tools/build_assets.py
"""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
STYLE = """
text{font-family:'Segoe UI',Arial,sans-serif}
.mono{font-family:Consolas,'Liberation Mono',monospace}
.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 36s linear infinite}
.pulse{animation:pulse 5s ease-in-out infinite}
.scan{animation:scan 12s ease-in-out infinite}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:.42}50%{opacity:1}}
@keyframes scan{0%,100%{transform:translateX(0);opacity:0}15%,75%{opacity:.65}85%{transform:translateX(950px);opacity:0}}
@media(prefers-reduced-motion:reduce){.orbit,.pulse,.scan{animation:none}.scan{display:none}}
"""


def svg(w, h, title, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Dark technical layout with cyan and violet accents. Decorative slow orbit and scanning motion; reduced-motion supported.</desc>
<defs>
 <linearGradient id="edge"><stop stop-color="#59eadb"/><stop offset=".55" stop-color="#5077be"/><stop offset="1" stop-color="#ba91ff"/></linearGradient>
 <radialGradient id="halo"><stop stop-color="#234962" stop-opacity=".58"/><stop offset="1" stop-color="#09101b" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1c2c3e" stroke-width=".7"/></pattern>
 <clipPath id="frame"><rect width="{w}" height="{h}" rx="12"/></clipPath>
</defs>
<style>{STYLE}</style>
<g clip-path="url(#frame)">
 <rect width="{w}" height="{h}" fill="#090f19"/>
 <rect width="{w}" height="{h}" fill="url(#grid)" opacity=".45"/>
 {content}
 <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="#29394d"/>
 <path d="M1 36V1H90M{w-90} {h-1}H{w-1}V{h-36}" fill="none" stroke="url(#edge)" stroke-width="2"/>
</g></svg>
'''


def text(x, y, value, size=16, color="#a6b8ce", extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{escape(value)}</text>'


def orbital(cx, cy, radius=124):
    out = f'<circle cx="{cx}" cy="{cy}" r="{radius*1.9}" fill="url(#halo)"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#2c475d"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{radius-26}" fill="none" stroke="#244d5d" stroke-dasharray="2 9"/>'
    out += f'<circle class="orbit" cx="{cx}" cy="{cy}" r="{radius+12}" fill="none" stroke="#72ebdc" stroke-width="2" stroke-dasharray="65 340 18 500"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{radius-52}" fill="#0d1725" stroke="#3c4b67"/>'
    for deg in (30, 150, 270):
        angle = math.radians(deg)
        x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        out += f'<path d="M{cx} {cy}L{x:.1f} {y:.1f}" stroke="#29435b"/>'
        out += f'<circle class="pulse" cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#65e5da"/>'
    out += text(cx, cy+17, "S/52", 42, "#edf8ff", 'text-anchor="middle" font-weight="700"')
    out += text(cx, cy+41, "SYSTEM BUILDER", 10, "#7ca2b5", 'class="mono" text-anchor="middle" letter-spacing="1"')
    return out


def hero(compact=False):
    w, h = (700, 470) if compact else (1200, 460)
    body = text(42, 48, "SAMUEL521199 / PUBLIC LAB", 15, "#65e5da", 'class="mono" letter-spacing="2"')
    if compact:
        body += text(42, 148, "SAMUEL", 84, "#f0f6fc", 'font-weight="750" letter-spacing="-3"')
        body += text(42, 206, "把想法，构建成系统。", 30, "#d3e2f1")
        body += text(42, 262, "AI SYSTEMS  /  WORKFLOWS", 18, "#ae98ec", 'class="mono"')
        body += text(42, 293, "GAMES  /  CREATIVE TOOLS", 18, "#ae98ec", 'class="mono"')
        body += '<path d="M42 335H658" stroke="#25364a"/>'
        body += text(42, 381, "BUILD SYSTEMS. MAKE THEM REAL.", 22, "#eef4ff", 'class="mono"')
        body += text(42, 430, "SOURCE CODE  →  DESIGN NOTES  →  ITERATION", 14, "#8da5bf", 'class="mono"')
    else:
        body += orbital(980, 218)
        body += text(42, 170, "SAMUEL", 104, "#f0f6fc", 'font-weight="750" letter-spacing="-4"')
        body += text(46, 226, "把想法，构建成系统。", 30, "#d3e2f1")
        body += text(46, 278, "AI SYSTEMS / WORKFLOWS / CREATIVE TOOLS", 18, "#b49bf0", 'class="mono"')
        body += text(46, 326, "BUILD SYSTEMS. MAKE THEM REAL.", 19, "#a6b8ce", 'class="mono" letter-spacing="1"')
        body += '<path d="M42 378H1158" stroke="#25364a"/>'
        body += text(42, 422, "01 / THINK IN SYSTEMS", 14, "#83bdbd", 'class="mono"')
        body += text(433, 422, "02 / BUILD IN CODE", 14, "#83bdbd", 'class="mono"')
        body += text(810, 422, "03 / KEEP ITERATING", 14, "#b09ccf", 'class="mono"')
    body += f'<rect class="scan" x="0" y="0" width="2" height="{h}" fill="#72eedc" opacity=".1"/>'
    return svg(w, h, "Samuel — AI systems, workflows and creative tools", body)


def flagship():
    body = text(34, 43, "01 / CURRENT FOCUS", 15, "#65e5da", 'class="mono" letter-spacing="2"')
    body += text(34, 103, "JARVIS SYSTEM", 52, "#f0f6fc", 'font-weight="700" letter-spacing="-1"')
    body += text(36, 146, "A personal AI assistant, built around continuity.", 20, "#a8bbd1")
    body += text(36, 194, "MEMORY  /  CONVERSATION  /  TOOLS  /  WORKSPACE", 15, "#ba9dec", 'class="mono"')
    body += '<path d="M36 222H1164" stroke="#27384c"/>'
    body += text(36, 258, "PYTHON + WEB UI", 14, "#8ea9c1", 'class="mono"')
    body += text(1164, 258, "DEVELOPMENT PROTOTYPE  ↗", 14, "#65e5da", 'class="mono" text-anchor="end"')
    for i, (label, y) in enumerate([("CONTEXT", 62), ("MEMORY", 112), ("ACTION", 162)]):
        body += f'<path d="M875 {y}H925" stroke="#46677d"/>'
        body += f'<rect x="925" y="{y-17}" width="228" height="34" rx="5" fill="#0e1b29" stroke="#314d65"/>'
        body += text(944, y+5, label, 14, "#92c9cc", 'class="mono"')
        body += f'<circle class="pulse" cx="1132" cy="{y}" r="3" fill="#7ce0d5" style="animation-delay:{i}s"/>'
    body += '<path d="M875 62V162" stroke="#46677d"/>'
    return svg(1200, 284, "JarvisSystem — personal AI assistant development prototype", body)


def card(number, name, category, subtitle, stack, accent):
    body = text(26, 37, f"{number} / {category}", 13, accent, 'class="mono" letter-spacing="1"')
    body += text(26, 90, name, 36, "#eff5fc", 'font-weight="700" letter-spacing="-1"')
    body += text(26, 128, subtitle, 16, "#a6b8ce")
    body += '<path d="M26 154H548" stroke="#27384c"/>'
    body += text(26, 188, stack, 13, "#b3c1d2", 'class="mono"')
    body += text(548, 188, "↗", 24, accent, 'text-anchor="end"')
    return svg(574, 214, name+" — "+subtitle, body)


(ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
(ASSETS / "hero-compact.svg").write_text(hero(True), encoding="utf-8")
(ASSETS / "jarvis.svg").write_text(flagship(), encoding="utf-8")
(ASSETS / "structforge.svg").write_text(card("02", "StructForge", "WORKFLOW ENGINE", "Visual orchestration for AI workflows.", "GO / VUE / TYPESCRIPT", "#67e5d8"), encoding="utf-8")
(ASSETS / "wordfront.svg").write_text(card("03", "WORD FRONT", "LEARNING × PLAY", "Tactical cards meet vocabulary practice.", "JAVASCRIPT / ELECTRON / FSRS", "#ba9dec"), encoding="utf-8")
(ASSETS / "footer.svg").write_text(svg(1200, 84,
    "Built from public projects, documented in code",
    text(32, 49, "IDEA → ARCHITECTURE → CODE → ITERATION", 17, "#91b8c9", 'class="mono"')
    + text(1164, 49, "SAMUEL / BUILD LOG", 15, "#c0a6ed", 'class="mono" text-anchor="end"')), encoding="utf-8")
print("Built 6 SVG assets.")
