# Spiritual AI Reviews

Static publication for `https://spirirtualaireviews.store` (the domain spelling supplied by the owner). No dependencies, accounts, or tracking scripts.

## Edit and preview

Articles and shared layout live in `build.py`; styling lives in `style.css`.

```sh
python3 build.py
python3 check.py
python3 -m http.server 8080 --bind 127.0.0.1
```

Open http://localhost:8080/. Python serves directory indexes; deployed hosting must do the same. Configure the host to serve `404.html` with HTTP 404 for unknown paths.

## Deployment handoff

Deploy the generated `index.html`, `articles/`, `topics/`, `about/`, `editorial-policy/`, `privacy/`, `404.html`, `style.css`, `favicon.svg`, `robots.txt`, and `sitemap.xml`. Keep the Python scripts and this README out of the public upload. No server-side application is needed.

Before deployment, confirm the exact registered domain spelling. If it differs, change `DOMAIN` in `build.py`, rebuild, and run the checks. Do not redirect article canonicals to product sites: every article has its own publication canonical.

Once a hosting provider is selected, complete its details on the privacy page. Then configure HTTPS and one preferred hostname, verify the domain in Search Console, submit `/sitemap.xml`, inspect representative URLs, and monitor impressions, clicks, and referrals. No ranking or rich-result eligibility is guaranteed by metadata.

## Editorial scope

Six launch articles cover self-understanding, learning, and business AI. Product overviews are based on public pages checked October 3, 2026, not independent hands-on tests. Ownership and AI assistance are disclosed. There are no invented testimonials, scores, or user-count claims. Review current product descriptions and prices when updating articles.
