# Arthur Yamin — Portfolio

A personal portfolio / CV site for **Arthur Yamin — Data & Quantitative Analyst**.

Built with plain **HTML, CSS, and vanilla JavaScript** — no build step, no dependencies.
Fast, accessible, responsive, with light/dark themes.

## Preview locally

```bash
cd portfolio
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy to GitHub Pages

1. Create a repository named **`<your-username>.github.io`** (e.g. `arturyamin.github.io`).
2. Push this folder's contents to it:

   ```bash
   cd portfolio
   git init
   git add .
   git commit -m "Portfolio site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
   git push -u origin main
   ```

3. Enable Pages: **Settings → Pages → Source: GitHub Actions** (the included
   `.github/workflows/deploy.yml` handles deployment automatically on every push).
4. Your site goes live at **`https://<your-username>.github.io`**.

> Alternatively, any repo works if you set the Pages source to the `main` branch
> and root `/` — the Actions workflow above is the recommended, zero-config route.

## Structure

```
portfolio/
├── index.html              # All page content (single page)
├── css/style.css           # Styling + light/dark themes + responsive
├── js/main.js              # Theme toggle, mobile nav, scroll reveal
├── assets/profile.jpg      # Headshot (shown on the website only)
├── build_pdf.py            # Generates the clean, link-rich CV PDF
├── cv.pdf                  # Generated output (auto-rebuilt — see below)
└── .github/workflows/deploy.yml   # GitHub Pages deployment + PDF rebuild
```

## The CV PDF (auto-generated)

**Primary download** is the Google Drive copy — the "Download CV (PDF)" button
links straight to the Drive document's PDF export.

`cv.pdf` is the **fallback**: a clean, **AI-readable** version of the CV (no
photo, no website chrome, but with **real clickable links** — email, phone,
LinkedIn, GitHub), generated from this site and offered as a direct-file
alternative when the Drive link is unavailable.

**It rebuilds automatically** whenever the site changes, via two mechanisms:

1. **Locally** — a git `post-commit` hook (`.git/hooks/post-commit`) runs
   `build_pdf.py` after every commit and stages the fresh `cv.pdf`.
2. **On push** — the GitHub Actions workflow installs WeasyPrint and regenerates
   `cv.pdf` before deploying, so the published site always has a current PDF.

To rebuild manually:

```bash
pip install weasyprint
python3 build_pdf.py            # writes ./cv.pdf
```

> Note: the local hook lives in `.git/hooks/` and is **not** committed. If you
> clone this repo elsewhere, re-create it (or just rely on the CI rebuild, which
> is the source of truth for the published PDF).

## Customizing

- **Content** — edit `index.html`. Each section (About, Skills, Experience,
  Projects, Education, Contact) is a self-contained `<section>`.
- **Colors / fonts** — edit the design tokens at the top of `css/style.css`
  (`:root` and `[data-theme="dark"]`).
- **Photo** — add a headshot to `assets/` and reference it in the hero.
- **Links** — update the email, LinkedIn, and GitHub URLs in the Contact section.
