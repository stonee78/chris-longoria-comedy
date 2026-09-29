"""
Refresh the Merch section of index.html from Chris's Big Cartel shop.

Big Cartel publishes every shop's products at /products.json (public, no key).
The shop sends no CORS header, so the site can't read it in the browser; this
script writes the cards and the Product markup into index.html between the
MERCH markers instead. Run by .github/workflows/update-merch.yml once a day;
it only changes the file when the shop changed. Checkout stays on Big Cartel.

    python tools/update_merch.py            # update index.html
    python tools/update_merch.py --check    # print what it would write, change nothing
"""
import html, json, os, re, sys, urllib.request

SHOP = "https://chrislongoriacomedy.bigcartel.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
START = "<!-- MERCH:START (generated from Big Cartel by tools/update_merch.py; do not edit by hand) -->"
END = "<!-- MERCH:END -->"


def products():
    req = urllib.request.Request(SHOP + "/products.json", headers={"User-Agent": "Mozilla/5.0 (chrislongoriacomedy.com merch sync)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def image(p):
    imgs = p.get("images") or []
    if not imgs:
        return None, 600, 600
    url = re.sub(r"\?.*$", "", imgs[0]["url"]) + "?auto=format&fit=max&w=600&h=600"
    w, h = imgs[0].get("width") or 600, imgs[0].get("height") or 600
    scale = 600 / max(w, h)
    return url, round(w * scale), round(h * scale)


def build(items):
    cards, ld = [], []
    for p in items:
        if p.get("status") != "active" or p.get("has_password_protection"):
            continue
        name = html.escape(p["name"])
        url = SHOP + p["url"]
        opts = p.get("options") or []
        in_stock = any(not o.get("sold_out") for o in opts) if opts else True
        img, w, h = image(p)
        price = f"${p['price']:,.2f}".replace(".00", "")
        img_tag = f'<img src="{html.escape(img)}" alt="{name}" width="{w}" height="{h}" loading="lazy">' if img else ""
        action = '<span class="btn solid">Buy</span>' if in_stock else '<span class="sold-out">Sold out</span>'
        cards.append(f'        <a class="merch-card" href="{url}" target="_blank" rel="noopener">{img_tag}<h3>{name}</h3><p class="price">{price}</p>{action}</a>')
        ld.append({"@type": "Product", "name": p["name"], "image": img, "url": url,
                   "description": re.sub(r"\s+", " ", p.get("description") or "").strip()[:300] or p["name"],
                   "brand": {"@type": "Brand", "name": "Chris Longoria Comedy"},
                   "offers": {"@type": "Offer", "price": f"{p['price']:.2f}", "priceCurrency": "USD", "url": url,
                              "availability": "https://schema.org/InStock" if in_stock else "https://schema.org/OutOfStock"}})
    grid = "\n".join(['      <div class="merch-grid">'] + cards + ["      </div>"]) if cards else '      <p class="no-shows">New merch is on the way.</p>'
    script = '      <script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": x} for i, x in enumerate(ld)]}, ensure_ascii=False) + "</script>"
    return START + "\n" + grid + ("\n" + script if ld else "") + "\n" + END, len(cards)


def main():
    block, n = build(products())
    page = open(INDEX, encoding="utf-8").read()
    new, count = re.subn(re.escape(START) + ".*?" + re.escape(END), lambda _: block, page, flags=re.S)
    if count != 1:
        sys.exit("MERCH markers not found exactly once in index.html")
    if "--check" in sys.argv:
        print(block); return
    if new == page:
        print(f"no change ({n} items)"); return
    open(INDEX, "w", encoding="utf-8", newline="\n").write(new)
    print(f"updated: {n} items")


if __name__ == "__main__":
    main()
