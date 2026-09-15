# Jiaqi Liu — Portfolio

Portfolio website for [jiaqiliu.com](https://jiaqiliu.com).

## Website

`site/` is the production and deployment root. The website uses plain static HTML, CSS, and JavaScript, with no build step and no npm, Python, or package installation required. Edit its HTML/CSS/JS files directly.

## Local preview

```sh
cd site
python3 -m http.server 8000
```

Open http://localhost:8000/. Python is only an optional local HTTP server, not a website dependency. Use HTTP preview so root-relative links resolve correctly.

## Hosting

Publish `site/` directly at https://jiaqiliu.com with no build command. Support directory index pages and serve `404.html` with an HTTP 404 status for unknown routes.

- `/` is the canonical homepage; `/projects` is a compatibility alias canonicalized to `/`.
- A custom `404.html`, `robots.txt`, and `sitemap.xml` are included.
- Vimeo and YouTube embeds require those external services.
