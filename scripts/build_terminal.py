"""Generate the animated terminal SVGs used as the profile README hero.

Usage: python3 scripts/build_terminal.py
Writes assets/terminal/{en,es}-{dark,light}.svg. Standard library only.

Every text run is pinned to a fixed character grid with textLength, so box
drawing and columns stay aligned whatever monospace font the viewer has.
"""

from pathlib import Path
from xml.sax.saxutils import escape

COLS = 92
CW = 8.4  # character cell width in px
LH = 20  # line height in px
PAD = 24
TOP = 44  # window chrome height
FONT = 14
WIDTH = round(PAD * 2 + COLS * CW)

THEMES = {
    "dark": {
        "bg": "#0d1117", "chrome": "#161b22", "border": "#30363d",
        "frame": "#3d5a8a", "path": "#78a7ff", "cmd": "#e6edf3", "out": "#c9d1d9",
        "muted": "#8b949e", "accent": "#78a7ff", "key": "#f2cc60", "ok": "#7ee787",
        "name_from": "#78a7ff", "name_to": "#c2d6ff",
    },
    "light": {
        "bg": "#ffffff", "chrome": "#f6f8fa", "border": "#d0d7de",
        "frame": "#9fb3d9", "path": "#1748c7", "cmd": "#1f2328", "out": "#24292f",
        "muted": "#57606a", "accent": "#1748c7", "key": "#9a6700", "ok": "#1a7f37",
        "name_from": "#1748c7", "name_to": "#4f7ae0",
    },
}

# 5-row pixel font for the banner.
GLYPHS = {
    "A": [".##.", "#..#", "####", "#..#", "#..#"],
    "L": ["#...", "#...", "#...", "#...", "####"],
    "E": ["####", "#...", "###.", "#...", "####"],
    "X": ["#..#", "#..#", ".##.", "#..#", "#..#"],
    "G": [".###", "#...", "#.##", "#..#", ".###"],
    "U": ["#..#", "#..#", "#..#", "#..#", ".##."],
    "T": ["###", ".#.", ".#.", ".#.", ".#."],
    " ": ["..", "..", "..", "..", ".."],
}

CONTENT = {
    "en": {
        "title": "alex@kanazawa-dev: ~",
        "tagline": [("AI Software Engineer", "accent"), (" · Indie Builder", "out")],
        "motto": "Ship something people actually use.",
        "blocks": [
            ("whoami", [
                [("Alex Elgueta", "accent"), (" · software engineer and product builder · Los Ángeles, Chile", "out")],
                [("I build products end to end: architecture, backend, interfaces, and the infra", "out")],
                [("that ships them. Lately, most of them put AI to work on real data.", "out")],
            ]),
            ("alex --now", [
                [("▸ ", "key"), ("Karibu    ", "accent"), ("Software Engineer · my main job · building Titvo and AI products", "out")],
                [("▸ ", "key"), ("ComuniOS  ", "accent"), ("Founder, CEO & CTO · condominium management for Chile", "out")],
                [("▸ ", "key"), ("Voysse    ", "accent"), ("white-label AI agents · WhatsApp, web chat, RAG, MCP", "out")],
            ]),
            ("git log --author=alex --contributions", [
                [("★ ", "key"), ("diri      ", "accent"), ("Rust · run fifty coding agents in parallel, review in one place", "out")],
                [("★ ", "key"), ("Defi      ", "accent"), ("Swift · fast, native scrollable-tiling window manager for macOS", "out")],
                [("Excited to be a contributor to both.", "ok")],
            ]),
            ("alex --experience --table", "table"),
            ("alex --stack", [
                [("lang   ", "muted"), ("⚙ TypeScript  ⚙ Python  ⚙ Rust", "out")],
                [("build  ", "muted"), ("⚙ React  ⚙ Next.js  ⚙ NestJS  ⚙ FastAPI  ⚙ PostgreSQL  ⚙ Docker", "out")],
                [("ship   ", "muted"), ("⚙ Railway  ⚙ Vercel  ⚙ AWS  ⚙ Cloudflare", "out")],
            ]),
            ("cat values.txt", [
                [("Simple systems. Clean architecture. Shipping useful software.", "ok")],
            ]),
            ("grep -i contact info.txt", [
                [("web ", "muted"), ("alexelgueta.me   ", "out"), ("x ", "muted"), ("@AlexElguetaDev   ", "out"),
                 ("in ", "muted"), ("linkedin.com/in/alexelguetar", "out")],
            ]),
        ],
        "table": (
            ["Company", "Role", "Period"],
            [
                ["Karibu (main job)", "Software Engineer", "2026 – now"],
                ["ComuniOS", "Founder, CEO & CTO", "2026 – now"],
                ["Portal de Especialistas", "CTO & Co-Founder", "2025 – 2026"],
                ["Lolocar", "Full Stack & Front End Lead", "2023 – 2025"],
                ["Zephron Software", "Software Engineer", "2022 – 2025"],
                ["NextStep", "Co-Founder & Tech Lead", "2023"],
                ["Devsafio", "Full Stack Developer", "2023"],
                ["Freelancer.com", "Full Stack Developer", "2021 – 2023"],
                ["PedidosYa", "Developer", "2019 – 2022"],
            ],
        ),
        "alt": "Animated terminal introducing Alex Elgueta, AI Software Engineer and Indie Builder",
    },
    "es": {
        "title": "alex@kanazawa-dev: ~",
        "tagline": [("AI Software Engineer", "accent"), (" · Indie Builder", "out")],
        "motto": "Crear algo que la gente realmente use.",
        "blocks": [
            ("whoami", [
                [("Alex Elgueta", "accent"), (" · ingeniero de software y creador de productos · Los Ángeles, Chile", "out")],
                [("Construyo productos de punta a punta: arquitectura, backend, interfaces e infra", "out")],
                [("que los pone en producción. Hoy, casi todos ponen la IA a trabajar con datos reales.", "out")],
            ]),
            ("alex --now", [
                [("▸ ", "key"), ("Karibu    ", "accent"), ("ingeniero de software · mi trabajo principal · Titvo y productos con IA", "out")],
                [("▸ ", "key"), ("ComuniOS  ", "accent"), ("fundador, CEO y CTO · administración de condominios en Chile", "out")],
                [("▸ ", "key"), ("Voysse    ", "accent"), ("agentes de IA de marca blanca · WhatsApp, chat web, RAG, MCP", "out")],
            ]),
            ("git log --author=alex --contributions", [
                [("★ ", "key"), ("diri      ", "accent"), ("Rust · cincuenta agentes de código en paralelo, todo en un lugar", "out")],
                [("★ ", "key"), ("Defi      ", "accent"), ("Swift · gestor de ventanas en mosaico, rápido y nativo para macOS", "out")],
                [("Feliz y emocionado de contribuir a ambos.", "ok")],
            ]),
            ("alex --experience --table", "table"),
            ("alex --stack", [
                [("lenguajes  ", "muted"), ("⚙ TypeScript  ⚙ Python  ⚙ Rust", "out")],
                [("desarrollo ", "muted"), ("⚙ React  ⚙ Next.js  ⚙ NestJS  ⚙ FastAPI  ⚙ PostgreSQL  ⚙ Docker", "out")],
                [("despliegue ", "muted"), ("⚙ Railway  ⚙ Vercel  ⚙ AWS  ⚙ Cloudflare", "out")],
            ]),
            ("cat valores.txt", [
                [("Sistemas simples. Arquitectura limpia. Software útil en producción.", "ok")],
            ]),
            ("grep -i contacto info.txt", [
                [("web ", "muted"), ("alexelgueta.me   ", "out"), ("x ", "muted"), ("@AlexElguetaDev   ", "out"),
                 ("in ", "muted"), ("linkedin.com/in/alexelguetar", "out")],
            ]),
        ],
        "table": (
            ["Empresa", "Rol", "Período"],
            [
                ["Karibu (principal)", "Ingeniero de software", "2026 – hoy"],
                ["ComuniOS", "Fundador, CEO y CTO", "2026 – hoy"],
                ["Portal de Especialistas", "CTO y cofundador", "2025 – 2026"],
                ["Lolocar", "Full Stack y Front End Lead", "2023 – 2025"],
                ["Zephron Software", "Ingeniero de software", "2022 – 2025"],
                ["NextStep", "Cofundador y Tech Lead", "2023"],
                ["Devsafio", "Desarrollador full stack", "2023"],
                ["Freelancer.com", "Programador full stack", "2021 – 2023"],
                ["PedidosYa", "Programador", "2019 – 2022"],
            ],
        ),
        "alt": "Terminal animada que presenta a Alex Elgueta, AI Software Engineer e Indie Builder",
    },
}


def table_lines(header, rows):
    widths = [max(len(r[i]) for r in [header, *rows]) + 2 for i in range(len(header))]

    def border(left, mid, right):
        return [(left + mid.join("═" * w for w in widths) + right, "frame")]

    def row(cells, cls):
        out = [("║", "frame")]
        for cell, w in zip(cells, widths):
            out += [(" " + cell.ljust(w - 1), cls), ("║", "frame")]
        return out

    lines = [border("╔", "╦", "╗"), row(header, "key"), border("╠", "╬", "╣")]
    lines += [row(r, "out") for r in rows]
    lines.append(border("╚", "╩", "╝"))
    return lines


def prompt_lines(index, command):
    left = "┌─(~/github)"
    right = "(alex@kanazawa)─┐"
    top = [("┌─(", "frame"), ("~/github", "path"), (")", "frame"),
           ("─" * (COLS - len(left) - len(right)), "frame"),
           ("(", "frame"), ("alex@kanazawa", "path"), (")─┐", "frame")]
    stamp = f"00:00:{index:02d}"
    start = f"└─({stamp})──○ "
    end = "○──(zsh)─┘"
    bottom_prefix = [("└─(", "frame"), (stamp, "muted"), (")──○ ", "frame")]
    bottom_suffix = [(" " * (COLS - len(start) - len(command) - len(end)), "frame"), (end, "frame")]
    return top, bottom_prefix, command, bottom_suffix


class Svg:
    def __init__(self):
        self.parts = []

    def typed(self, col, row_y, chunk, cls, start, per_char):
        """Reveal chunk one character at a time; returns next column."""
        for i, ch in enumerate(chunk):
            if ch != " ":
                self.text(col + i, row_y, [(ch, cls)], delay=start + i * per_char)
        return col + len(chunk)

    def text(self, col, row_y, segments, delay=None):
        """Place segments on the grid starting at column col; returns next column."""
        for chunk, cls in segments:
            if not chunk:
                continue
            x = PAD + col * CW
            style = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
            klass = f"{cls} r" if delay is not None else cls
            self.parts.append(
                f'<text x="{x:.1f}" y="{row_y}" class="{klass}" textLength="{len(chunk) * CW:.1f}" '
                f'lengthAdjust="spacingAndGlyphs"{style}>{escape(chunk)}</text>'
            )
            col += len(chunk)
        return col


def banner(svg, y, theme_name):
    pixel, gap = 7, 1
    x = PAD
    cells = []
    for ch in "ALEX ELGUETA":
        glyph = GLYPHS[ch]
        for r, line in enumerate(glyph):
            for c, bit in enumerate(line):
                if bit == "#":
                    cells.append((x + c * pixel, y + r * pixel))
        x += (len(glyph[0]) + gap) * pixel
    rects = "".join(f'<rect x="{cx}" y="{cy}" width="{pixel - 1}" height="{pixel - 1}" rx="1"/>' for cx, cy in cells)
    svg.parts.append(f'<g fill="url(#name-{theme_name})" class="sweep">{rects}</g>')
    return x


def build(lang, theme_name):
    content, theme = CONTENT[lang], THEMES[theme_name]
    svg = Svg()
    y = TOP + PAD

    banner_right = banner(svg, y, theme_name)
    tag_col = int((banner_right - PAD) / CW) + 3
    svg.text(tag_col, y + 14, content["tagline"], delay=0.9)
    svg.text(tag_col, y + 33, [(content["motto"], "muted")], delay=1.05)
    y += 5 * 7 + LH + 6

    t = 1.3
    for index, (command, output) in enumerate(content["blocks"], start=1):
        y += LH
        top, prefix, cmd, suffix = prompt_lines(index, command)
        svg.text(0, y, top, delay=t)
        y += LH
        col = svg.text(0, y, prefix, delay=t)
        type_time = len(cmd) * 0.04
        col = svg.typed(col, y, cmd, "cmd", t + 0.15, 0.04)
        svg.text(col, y, suffix, delay=t)
        t += 0.15 + type_time + 0.15
        lines = table_lines(*content["table"]) if output == "table" else output
        for line in lines:
            y += LH
            svg.text(0, y, line, delay=t)
            t += 0.06
        y += LH // 2
        t += 0.3

    y += LH
    top, prefix, _, _ = prompt_lines(len(content["blocks"]) + 1, "")
    svg.text(0, y, top, delay=t)
    y += LH
    col = svg.text(0, y, prefix, delay=t)
    cursor_x = PAD + col * CW
    svg.parts.append(
        f'<rect x="{cursor_x:.1f}" y="{y - 13}" width="{CW:.1f}" height="16" class="cursor" '
        f'style="animation:show .01s {t:.2f}s both, blink 1s step-end {t:.2f}s infinite"/>'
    )

    height = y + PAD
    dots = "".join(
        f'<circle cx="{PAD + i * 20}" cy="{TOP / 2}" r="6" fill="{c}"/>'
        for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"])
    )
    classes = "".join(
        f".{k}{{fill:{v}}}" for k, v in theme.items() if k in {"frame", "path", "cmd", "out", "muted", "accent", "key", "ok"}
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(content["alt"])}</title>
<defs><linearGradient id="name-{theme_name}" x1="0" x2="1"><stop offset="0" stop-color="{theme["name_from"]}"/><stop offset="1" stop-color="{theme["name_to"]}"/></linearGradient></defs>
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FONT}px;white-space:pre}}
{classes}
.accent{{font-weight:700}}
.cursor{{fill:{theme["accent"]}}}
.r{{animation:show .01s both}}
.sweep{{animation:sweep .9s steps(56) .2s both}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes sweep{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="12" fill="{theme["bg"]}" stroke="{theme["border"]}"/>
<path d="M12.5 .5h{WIDTH - 25}a12 12 0 0 1 12 12v{TOP - 12}h-{WIDTH - 1}v-{TOP - 12}a12 12 0 0 1 12-12z" fill="{theme["chrome"]}"/>
<line x1=".5" y1="{TOP + .5}" x2="{WIDTH - .5}" y2="{TOP + .5}" stroke="{theme["border"]}"/>
{dots}
<text x="{WIDTH / 2}" y="{TOP / 2 + 5}" text-anchor="middle" class="muted">{escape(content["title"])}</text>
{chr(10).join(svg.parts)}
</svg>
"""


def main():
    for lang, content in CONTENT.items():
        for command, output in content["blocks"]:
            lines = table_lines(*content["table"]) if output == "table" else output
            for line in lines:
                width = sum(len(chunk) for chunk, _ in line)
                if width > COLS:
                    raise SystemExit(f"{lang}: line exceeds {COLS} columns ({width}): {line}")
    out_dir = Path(__file__).resolve().parent.parent / "assets" / "terminal"
    out_dir.mkdir(parents=True, exist_ok=True)
    for lang in CONTENT:
        for theme_name in THEMES:
            (out_dir / f"{lang}-{theme_name}.svg").write_text(build(lang, theme_name), encoding="utf-8")


if __name__ == "__main__":
    main()
