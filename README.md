# chrislongoriacomedy.com

Chris Longoria's comedy site, built and hosted by Belleeah's Apples & Treats as part of its sponsorship of That Dude Talks. Plain HTML, CSS and JavaScript with no build step, served by GitHub Pages.

## Files

- `index.html`: the page, including the search description, share preview tags and the Person markup that ties Chris's accounts together for search engines.
- `styles.css`, `main.js`: styling, click-to-load YouTube players, and the show list.
- `shows.json`: upcoming shows. Past dates hide themselves, and each show gets a Belleeah sponsor tag plus event markup automatically.
- `assets/`: Chris's stage photo, the share preview image (`og.jpg`, 1200x630) and the Belleeah logo (the cropped logo file from the Belleeah brand guidelines).

## Adding a show

Add an entry to `shows.json` and push:

```json
{ "date": "2026-10-10", "time": "20:00", "utc_offset": "-05:00",
  "title": "Kiko's Comedy Night", "venue": "Kiko's Mexican Food Restaurant & Cantina",
  "address": "5514 Everhart Rd.", "city": "Corpus Christi, TX",
  "tickets": "https://..." }
```

`time` and `doors` are 24-hour local time. `utc_offset` is -05:00 while Daylight Saving Time is in effect and -06:00 after it ends. `presenter` is optional.

Then run `python tools/update_shows.py`. It writes the upcoming shows into `index.html` as ComedyEvent markup (search engines trust markup in the page itself more than markup added by a script) and bumps the sitemap date. Commit `shows.json`, `index.html` and `sitemap.xml` together. Rerun it now and then even without changes, so past shows drop out of the markup.

## Search

- `robots.txt` and `sitemap.xml` at the root.
- Google Search Console: the URL-prefix property `https://chrislongoriacomedy.com/` is verified by the file `googleef0af64065cbc96b.html`. **Don't delete that file**, or verification is lost. It's owned by Belleeah's `jarvis-search-console` service account, with belleeah@gmail.com added as an owner.
- Markup in `index.html`: WebSite, Person (`#chris`, with sameAs links to his profiles), FAQPage (matching the visible FAQ section), and the generated ComedyEvent block.

## Moving to chrislongoriacomedy.com

**Done 2026-09-28.** The domain is in Chris's GoDaddy account, and Belleeah manages its DNS through GoDaddy Delegate Access ("Products & Domains"). Belleeah's own GoDaddy API key can't reach delegated domains, so DNS changes go through the GoDaddy dashboard. The steps below are kept for reference.

1. Add a `CNAME` file containing `chrislongoriacomedy.com`, and set the custom domain in the repo's Pages settings.
2. DNS at GoDaddy: A records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus a CNAME for `www` pointing to `stonee78.github.io`.
3. In `index.html`, replace every `https://stonee78.github.io/chris-longoria-comedy/` with `https://chrislongoriacomedy.com/` and **delete the `noindex` line** (it keeps the preview out of Google so it can't compete with the real domain later).
4. Once the certificate is issued, turn on "Enforce HTTPS" in Pages settings.

## Merch (branch `merch`, waiting on Chris's Big Cartel inventory)
- The Merch section in `index.html` is generated from Chris's Big Cartel shop by `tools/update_merch.py`, which reads the shop's public `products.json` (no login or key) and writes cards plus Product markup between the `MERCH:START` and `MERCH:END` markers. Checkout stays on Big Cartel.
- `.github/workflows/update-merch.yml` runs it daily at 13:15 UTC (8:15 AM Central) and commits only when the shop changed. Scheduled workflows run only from the default branch, so nothing runs until `merch` is merged into `main`.
- To go live: merge `merch` into `main`, push, then run the workflow once by hand (Actions, "Update merch from Big Cartel", Run workflow) to confirm it can push and that Pages redeploys.
