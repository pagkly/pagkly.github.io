#!/usr/bin/env python3
"""
build_pdf.py — Generate a clean, AI-readable CV PDF from index.html.

Design goals:
  * No photo, no decorative UI (nav, buttons, terminal, gradients) — pure content.
  * Real, clickable hyperlinks (mailto:, tel:, https:) preserved in the PDF.
  * Compact, text-first layout that reads well to both humans and LLMs.

Usage:
  python3 build_pdf.py            # writes ./cv.pdf
  python3 build_pdf.py out.pdf    # writes to a custom path

Dependencies:
  pip install weasyprint
"""
import sys
import os
import re
import datetime

try:
    import weasyprint
except ImportError:
    sys.exit("weasyprint is required. Install with: pip install weasyprint")

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "index.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "cv.pdf")

# Print-only stylesheet: strips the website chrome and produces a document.
# Kept separate from style.css so the live site is unaffected.
PRINT_CSS = r"""
@page { size: A4; margin: 15mm 16mm; }

* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

html, body {
  background: #ffffff !important;
  color: #14171c !important;
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 10.5px;
  line-height: 1.5;
}

/* ---- Hide all website chrome ---- */
.nav, .theme-toggle, .nav__burger, .btn, #printBtn, .hero__cta,
.footer, .hero__media, .hero__photo-wrap, .hero__photo, .hero__card,
.hero::before, .section__eyebrow { display: none !important; }

/* Force every reveal element visible (no JS in PDF) */
.reveal { opacity: 1 !important; transform: none !important; }

/* ---- Hero becomes a clean header block ---- */
.hero { padding: 0 0 10px; }
.hero__inner { display: block; }
.hero__title { font-size: 20px; font-weight: 800; margin: 2px 0 6px; letter-spacing: -0.02em; }
.hero__title .grad {
  background: none; -webkit-background-clip: border-box; background-clip: border-box; color: #14171c;
}
.hero__sub { font-size: 10.5px; color: #333a45; margin: 0 0 8px; max-width: none; }
.hero__stats { display: flex; gap: 26px; margin: 0; }
.hero__stats li { display: flex; flex-direction: column; }
.hero__stats strong { font-size: 13px; font-weight: 800; color: #14171c; }
.hero__stats strong, .grad { background: none; -webkit-background-clip: border-box; color: #14171c; }
.hero__stats span { font-size: 8.5px; color: #5b6472; }

/* ---- Sections ---- */
.section { padding: 14px 0; }
.section--alt, .section--contact { background: #ffffff !important; }
.section__title { font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em;
  color: #14171c; border-bottom: 1.5px solid #14171c; padding-bottom: 4px; margin-bottom: 10px; }
.section__lead { font-size: 9.5px; color: #5b6472; margin-top: 0; }
.section__head { margin-bottom: 10px; }

/* ---- About ---- */
.about { display: block; }
.about__text p { font-size: 10px; color: #2a303a; margin-bottom: 7px; }
.about__text p strong { color: #14171c; }
.about__facts { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px; }
.fact { display: flex; align-items: center; gap: 8px; border: 1px solid #d8dce3; border-radius: 6px;
  padding: 7px 10px; background: #f7f8fa; }
.fact__icon { font-size: 12px; }
.fact strong { font-size: 9.5px; display: block; }
.fact span { font-size: 9px; color: #5b6472; }

/* ---- Skills ---- */
.skills { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.skill-group { border: 1px solid #d8dce3; border-radius: 6px; padding: 9px 11px; background: #fff; }
.skill-group__title { font-size: 10px; font-weight: 700; margin-bottom: 6px; }
.skill-group__title::before { display: none; }
.tags { display: flex; flex-wrap: wrap; gap: 4px; }
.tags li { font-size: 8.5px; padding: 2px 7px; border-radius: 999px; background: #eef1f5;
  border: 1px solid #d8dce3; color: #2a303a; }

/* ---- Projects ---- */
.projects { display: grid; grid-template-columns: 1fr; gap: 8px; }
.project-card { border: 1px solid #d8dce3; border-radius: 6px; padding: 10px 12px; background: #fff; }
.project-card__top { display: flex; gap: 8px; margin-bottom: 6px; }
.project-card__icon { display: none; }
.project-card__title { font-size: 11px; font-weight: 700; }
.project-card__org { font-size: 8.5px; color: #5b6472; font-family: "JetBrains Mono", monospace; }
.project-card__points li { font-size: 9.5px; color: #2a303a; margin-bottom: 4px; padding-left: 14px; position: relative; }
.project-card__points li::before { content: "•"; position: absolute; left: 2px; color: #2563eb; }

/* ---- Experience timeline (flatten to a clean list) ---- */
.timeline { padding-left: 0; }
.timeline::before { display: none; }
.timeline__item { padding: 0 0 10px; }
.timeline__marker { display: none; }
.timeline__body { border: 1px solid #d8dce3; border-radius: 6px; padding: 10px 12px; background: #fff; }
.timeline__meta { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; margin-bottom: 6px; }
.timeline__role { font-size: 11px; font-weight: 700; }
.timeline__company { font-weight: 600; color: #2563eb; font-size: 10px; }
.timeline__loc { font-size: 9px; color: #5b6472; }
.timeline__date { margin-left: auto; font-size: 9px; color: #5b6472; font-family: "JetBrains Mono", monospace; }
.timeline__points li { font-size: 9.5px; color: #2a303a; margin-bottom: 4px; padding-left: 14px; position: relative; }
.timeline__points li::before { content: "•"; position: absolute; left: 2px; color: #2563eb; }
.timeline__points li strong { color: #14171c; }

/* ---- Education ---- */
.edu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.edu-card { border: 1px solid #d8dce3; border-radius: 6px; padding: 10px 12px; background: #fff; }
.edu-card__icon { display: none; }
.edu-card__title { font-size: 10.5px; font-weight: 700; margin-bottom: 3px; }
.edu-card__org { font-size: 9px; color: #2a303a; }
.edu-card__year { font-size: 9px; color: #2563eb; font-family: "JetBrains Mono", monospace; margin-top: 4px; }
.edu-card__note { font-size: 8.5px; color: #5b6472; margin-top: 4px; }
.edu-card__list { margin-top: 6px; }
.edu-card__list li { font-size: 9px; color: #2a303a; margin-bottom: 3px; padding-left: 12px; position: relative; }
.edu-card__list li::before { content: "•"; position: absolute; left: 0; color: #2563eb; }

/* ---- Contact: keep links, make them real & visible ---- */
.contact { display: block; }
.contact__inner { border: 1px solid #d8dce3; border-radius: 6px; padding: 14px 16px; text-align: left; background: #fff; }
.contact__inner .section__title { border: 0; }
.contact__lead { font-size: 9.5px; color: #5b6472; margin-bottom: 10px; }
.contact__links { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 0; }
.contact__link { display: flex; flex-direction: column; gap: 1px; border: 1px solid #d8dce3; border-radius: 6px;
  padding: 8px 10px; background: #f7f8fa; }
.contact__link-icon { display: none; }
.contact__link-label { font-size: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #5b6472; }
.contact__link-value { font-size: 9.5px; font-weight: 500; color: #2563eb; word-break: break-all; }

/* ---- Links: keep clickable, show as blue underlined text ---- */
a { color: #2563eb; text-decoration: underline; }
"""


def build(out_path: str) -> None:
    if not os.path.exists(INDEX):
        sys.exit(f"index.html not found at {INDEX}")

    html = open(INDEX, encoding="utf-8").read()

    # Inject the print-only stylesheet right after the existing <link> to style.css.
    style_link = '<link rel="stylesheet" href="css/style.css" />'
    if style_link in html:
        html = html.replace(
            style_link,
            style_link + f'\n  <style>\n{PRINT_CSS}\n  </style>',
        )
    else:
        # Fallback: inject before </head>
        html = html.replace("</head>", f"  <style>\n{PRINT_CSS}\n  </style>\n</head>")

    # Strip the profile image so no photo (or broken image box) appears in the PDF.
    html = html.replace('<img class="hero__photo"', '<img data-strip class="hero__photo"')

    # Remove self-referential / action links so the PDF only carries real contact links.
    # (The "Download CV" buttons would otherwise become a link pointing at the PDF itself.)
    html = re.sub(r'<a[^>]*href="cv\.pdf"[^>]*>.*?</a>', '', html, flags=re.S)
    html = re.sub(r'<button[^>]*id="printBtn"[^>]*>.*?</button>', '', html, flags=re.S)

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    weasyprint.HTML(string=html, base_url=HERE).write_pdf(out_path)

    size = os.path.getsize(out_path)
    print(f"[build_pdf] wrote {out_path} ({size:,} bytes) — generated {stamp}")


if __name__ == "__main__":
    build(OUT)
