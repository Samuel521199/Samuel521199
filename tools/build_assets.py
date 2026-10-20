"""Build self-contained profile SVG typography and technical diagrams.
Run: python tools/build_assets.py
"""
from pathlib import Path
from html import escape
import math
import base64

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
STYLE = """
text{font-family:'Segoe UI',Arial,sans-serif}
.mono{font-family:Consolas,'Liberation Mono',monospace}
.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 36s linear infinite}
.pulse{animation:pulse 5s ease-in-out infinite}
.scan{animation:scan 12s ease-in-out infinite}
.rain{animation:rain 5s linear infinite}
.route{stroke-dasharray:12 18;animation:route 6s linear infinite}
@keyframes rain{from{transform:translateY(-100px)}to{transform:translateY(130px)}}
@keyframes route{to{stroke-dashoffset:-120}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:.42}50%{opacity:1}}
@keyframes scan{0%,100%{transform:translateX(0);opacity:0}15%,75%{opacity:.65}85%{transform:translateX(950px);opacity:0}}
@media(prefers-reduced-motion:reduce){.orbit,.pulse,.scan,.rain,.route{animation:none}.scan{display:none}}
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
    art = base64.b64encode((ASSETS / "mecha-source.png").read_bytes()).decode("ascii")
    art_height = 234 if compact else 400
    body = f'<image href="data:image/png;base64,{art}" x="0" y="0" width="{w}" height="{art_height}"/>'
    body += f'<defs><linearGradient id="veil"><stop stop-color="#090f19" stop-opacity=".48"/><stop offset=".5" stop-color="#090f19" stop-opacity=".15"/><stop offset="1" stop-color="#090f19" stop-opacity="0"/></linearGradient></defs><rect width="{w}" height="{art_height}" fill="url(#veil)"/>'
    body += text(42, 48, "SAMUEL521199 / PUBLIC LAB", 15, "#65e5da", 'class="mono" letter-spacing="2"')
    if compact:
        body += text(42, 148, "SAMUEL", 84, "#f0f6fc", 'font-weight="750" letter-spacing="-3"')
        body += text(42, 206, "把想法，构建成系统。", 30, "#d3e2f1")
        body += text(42, 262, "AI SYSTEMS  /  WORKFLOWS", 18, "#ae98ec", 'class="mono"')
        body += text(42, 293, "GAMES  /  CREATIVE TOOLS", 18, "#ae98ec", 'class="mono"')
        body += '<path d="M42 335H658" stroke="#25364a"/>'
        body += text(42, 381, "BUILD SYSTEMS. MAKE THEM REAL.", 22, "#eef4ff", 'class="mono"')
        body += text(42, 430, "SOURCE CODE  →  DESIGN NOTES  →  ITERATION", 14, "#8da5bf", 'class="mono"')
    else:
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


def mini(kind):
    body = ""
    if kind == "code":
        for col in range(18):
            x = 12 + col * 20
            body += f'<g class="rain" style="animation-duration:{4+col%5}s;animation-delay:-{col*.71}s">'
            for row in range(12):
                body += text(x, row*18, "10ABCDEF"[(row*3+col)%8], 12, "#65e5da",
                             f'class="mono" opacity="{.1 + (row%6)*.1}"')
            body += '</g>'
        title = "01 / CODE STREAM"
    elif kind == "core":
        body += '<g transform="translate(180 62)">'
        for radius, color in [(44, "#65e5da"), (32, "#ba9dec"), (20, "#38748c")]:
            body += f'<circle class="orbit" r="{radius}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="40 12 4 14"/>'
        body += '<path class="pulse" d="M-8-14H8L16 0 8 14H-8L-16 0Z" fill="#112c3b" stroke="#72f4df"/></g>'
        body += '<path d="M18 62H105M255 62H342" stroke="#3b526e"/><path class="route" d="M18 62H105M255 62H342" stroke="#65e5da"/>'
        title = "02 / CORE FIELD"
    else:
        body += '<path d="M26 66H88L110 32H235L260 66H334M88 66L110 99H235L260 66" fill="none" stroke="#2f445d" stroke-width="2"/>'
        body += '<path class="route" d="M26 66H88L110 32H235L260 66H334M88 66L110 99H235L260 66" fill="none" stroke="#b496f0" stroke-width="2"/>'
        for x,y in [(26,66),(110,32),(235,32),(110,99),(235,99),(334,66)]:
            body += f'<circle class="pulse" cx="{x}" cy="{y}" r="5" fill="#102437" stroke="#65e5da"/>'
        title = "03 / SIGNAL ROUTE"
    body += '<rect x="1" y="119" width="358" height="40" fill="#0b1421"/><path d="M16 119H344" stroke="#27384c"/>'
    body += text(18,145,title,13,"#aec5d8",'class="mono" letter-spacing="1"')
    return svg(360,160,title+" — decorative animation",body)


def build():
    outputs = {
        "hero.svg": hero(),
        "hero-compact.svg": hero(True),
        "jarvis.svg": flagship(),
        "structforge.svg": card("02", "StructForge", "WORKFLOW ENGINE", "Visual orchestration for AI workflows.", "GO / VUE / TYPESCRIPT", "#67e5d8"),
        "wordfront.svg": card("03", "WORD FRONT", "LEARNING × PLAY", "Tactical cards meet vocabulary practice.", "JAVASCRIPT / ELECTRON / FSRS", "#ba9dec"),
        "footer.svg": svg(1200, 84,
    "Built from public projects, documented in code",
    text(32, 49, "IDEA → ARCHITECTURE → CODE → ITERATION", 17, "#91b8c9", 'class="mono"')
    + text(1164, 49, "SAMUEL / BUILD LOG", 15, "#c0a6ed", 'class="mono" text-anchor="end"')),
    }
    for kind in ("code", "core", "signal"):
        outputs[f"module-{kind}.svg"] = mini(kind)
    for name, content in outputs.items():
        (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")
    print(f"Built {len(outputs)} SVG assets.")


if __name__ == "__main__":
    build()
