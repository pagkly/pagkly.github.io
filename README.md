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
├── assets/                 # Drop images here (e.g. a headshot)
└── .github/workflows/deploy.yml   # GitHub Pages deployment
```

## Customizing

- **Content** — edit `index.html`. Each section (About, Skills, Experience,
  Projects, Education, Contact) is a self-contained `<section>`.
- **Colors / fonts** — edit the design tokens at the top of `css/style.css`
  (`:root` and `[data-theme="dark"]`).
- **Photo** — add a headshot to `assets/` and reference it in the hero.
- **Links** — update the email, LinkedIn, and GitHub URLs in the Contact section.
