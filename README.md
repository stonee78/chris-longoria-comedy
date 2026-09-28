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

`time` is 24-hour local time. `utc_offset` is -05:00 while Daylight Saving Time is in effect and -06:00 after it ends.

## Moving to chrislongoriacomedy.com

**Done 2026-09-28.** The domain is in Chris's GoDaddy account, and Belleeah manages its DNS through GoDaddy Delegate Access ("Products & Domains"). Belleeah's own GoDaddy API key can't reach delegated domains, so DNS changes go through the GoDaddy dashboard. The steps below are kept for reference.

1. Add a `CNAME` file containing `chrislongoriacomedy.com`, and set the custom domain in the repo's Pages settings.
2. DNS at GoDaddy: A records for `@` pointing to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus a CNAME for `www` pointing to `stonee78.github.io`.
3. In `index.html`, replace every `https://stonee78.github.io/chris-longoria-comedy/` with `https://chrislongoriacomedy.com/` and **delete the `noindex` line** (it keeps the preview out of Google so it can't compete with the real domain later).
4. Once the certificate is issued, turn on "Enforce HTTPS" in Pages settings.
