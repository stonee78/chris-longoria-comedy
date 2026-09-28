"""Rebuild the event markup in index.html from shows.json.

Search engines read structured data most reliably when it is in the page itself,
so upcoming shows are written into index.html as ComedyEvent JSON-LD between the
EVENTS-LD markers. The visible show cards still come from shows.json through
main.js. Run this after every change to shows.json, then commit both files:

    python tools/update_shows.py

It also bumps the sitemap's lastmod to today.
"""
import datetime
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
START = "<!-- EVENTS-LD:START (generated from shows.json by tools/update_shows.py; do not edit by hand) -->"
END = "<!-- EVENTS-LD:END -->"


def event(show):
    offset = show.get("utc_offset", "")
    ev = {
        "@context": "https://schema.org",
        "@type": "ComedyEvent",
        "name": show["title"],
        "startDate": show["date"] + ("T" + show["time"] + offset if show.get("time") else ""),
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": show.get("venue", ""),
            "address": ", ".join(x for x in (show.get("address"), show.get("city")) if x),
        },
        "performer": {"@id": "https://chrislongoriacomedy.com/#chris"},
        "sponsor": {"@type": "Organization", "name": "Belleeah's Apples & Treats", "url": "https://belleeah.com/"},
        "image": "https://chrislongoriacomedy.com/assets/og.jpg",
    }
    if show.get("doors"):
        ev["doorTime"] = show["date"] + "T" + show["doors"] + offset
    if show.get("presenter"):
        ev["organizer"] = {"@type": "Organization", "name": show["presenter"]}
    if show.get("tickets"):
        ev["offers"] = {"@type": "Offer", "url": show["tickets"], "availability": "https://schema.org/InStock"}
    return ev


def main():
    today = datetime.date.today().isoformat()
    shows = json.loads((ROOT / "shows.json").read_text(encoding="utf-8")).get("shows", [])
    upcoming = sorted((s for s in shows if s["date"] >= today), key=lambda s: s["date"] + s.get("time", ""))
    block = START + "\n"
    if upcoming:
        block += '<script type="application/ld+json">\n' + json.dumps([event(s) for s in upcoming], indent=2, ensure_ascii=False) + "\n</script>\n"
    block += END

    page = ROOT / "index.html"
    html = page.read_text(encoding="utf-8")
    new, count = re.subn(re.escape(START) + ".*?" + re.escape(END), lambda _: block, html, flags=re.S)
    if count != 1:
        raise SystemExit("EVENTS-LD markers not found exactly once in index.html")
    page.write_text(new, encoding="utf-8")

    sitemap = ROOT / "sitemap.xml"
    sitemap.write_text(re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>" + today + "</lastmod>", sitemap.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{len(upcoming)} upcoming show(s) written to index.html; sitemap lastmod {today}")


if __name__ == "__main__":
    main()
