#!/usr/bin/env python3
"""Builds the ORLEX Global static pages from one shared template.
Run from the repo root:  python3 _build/gen.py
Never touches 01/ (QR label pages), etiket/ or CNAME."""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://orlexglobal.com"
GROUPS = json.load(open(os.path.join(ROOT, "_build", "groups.json"), encoding="utf-8"))
NREFS = sum(len(g["refs"]) for g in GROUPS)
E = html.escape

NAV = [("products.html", "Products"), ("manufacturing.html", "Manufacturing"),
       ("private-label.html", "Private label"), ("distributors.html", "Distributors"),
       ("certificates.html", "Certificates"), ("contact.html", "Contact")]

ICON = {
 "factory": '<svg viewBox="0 0 24 24"><path d="M3 21V10l5 3V10l5 3V7l8 4v10z"/><path d="M3 21h18M8 17h1M12 17h1M16 17h1"/></svg>',
 "doc": '<svg viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></svg>',
 "tag": '<svg viewBox="0 0 24 24"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
 "hand": '<svg viewBox="0 0 24 24"><path d="M4 12h4l3 3 5-5"/><path d="M20 12a8 8 0 1 1-16 0 8 8 0 0 1 16 0z"/></svg>',
 "globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
 "box": '<svg viewBox="0 0 24 24"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>',
 "pharm": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="15" rx="2"/><path d="M12 9v7M8.5 12.5h7M8 5V3h8v2"/></svg>',
 "store": '<svg viewBox="0 0 24 24"><path d="M3 9l1.5-5h15L21 9"/><path d="M4 9v11h16V9M3 9h18M9 20v-6h6v6"/></svg>',
 "tender": '<svg viewBox="0 0 24 24"><path d="M9 4h6v3H9z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/><path d="m9 14 2 2 4-4"/></svg>',
 "lang": '<svg viewBox="0 0 24 24"><path d="M4 5h9M8.5 3v2M6 9c1.5 3 4 5 7 6M11 5c-1 4-3.5 7-7 9"/><path d="m13 21 4-9 4 9M14.5 18h5"/></svg>',
 "qr": '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M21 14v.01M14 21h7v-4"/></svg>',
 "shield": '<svg viewBox="0 0 24 24"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
}

ARCS = '''<svg class="arcs draw" viewBox="0 0 600 600" aria-hidden="true">
<path d="M300 40a260 260 0 1 1-1 0" stroke="rgba(255,255,255,.08)" stroke-width="1"/>
<path d="M300 110a190 190 0 1 1-1 0" stroke="rgba(255,255,255,.10)" stroke-width="1"/>
<path d="M120 380a200 200 0 0 1 260-280" stroke="#EF7B00" stroke-width="3"/>
<path d="M520 230a200 200 0 0 1-250 260" stroke="#3A5FA0" stroke-width="3"/>
</svg>'''

def head(page, title, desc, extra=""):
    canon = SITE + "/" + ("" if page == "index.html" else page)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ORLEX">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/orlex-mark-512.png">
<meta name="theme-color" content="#0D3981">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="512x512" href="assets/img/orlex-mark-512.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
'''

def header(page):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="hdr">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="ORLEX home"><img src="assets/img/orlex-logo.png" alt="ORLEX Orthopedic Products" width="152" height="36"></a>
    <nav class="nav" aria-label="Main">{links}<a class="nav-cta" href="contact.html">Request the price list</a></nav>
    <div class="hdr-cta">
      <a class="tray-btn" href="contact.html" title="Your enquiry list"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/></svg><span class="lbl">Enquiry</span><span class="count" data-n="0">0</span></a>
      <a class="btn sm" href="contact.html" data-magnetic>Price list <span class="arr">&rarr;</span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
'''

DATA = ("assets/js/products-data.js", "assets/js/bodymap-data.js", "assets/js/site.js")

def footer(scripts=("assets/js/site.js",)):
    groups = "".join(f'<li><a href="products.html#{gid}">{E(n)}</a></li>' for gid, n in [
        ("knee-supports", "Knee supports"), ("corsets", "Corsets"), ("ankle-support-orthosis", "Ankle & foot"),
        ("hand-wrist-finger-splints", "Wrist & hand"), ("neck-collars", "Neck collars"), ("pediatric-products", "Pediatric")])
    sc = "".join(f'<script src="{s}" defer></script>' for s in scripts)
    return f'''</main>
<footer class="ftr">
  <div class="wrap">
    <div class="top">
      <div>
        <a class="logo" href="index.html"><img src="assets/img/orlex-logo.png" alt="ORLEX" width="126" height="30"></a>
        <p>Orthopaedic supports and orthoses, manufactured by Efamed Medical in Istanbul since 1993.</p>
      </div>
      <div><h4>Range</h4><ul>{groups}<li><a href="products.html">All {len(GROUPS)} groups &rarr;</a></li></ul></div>
      <div><h4>Company</h4><ul><li><a href="manufacturing.html">Manufacturing</a></li><li><a href="private-label.html">Private label / OEM</a></li><li><a href="distributors.html">Become a distributor</a></li><li><a href="certificates.html">Certificates</a></li><li><a href="https://www.orlex.com.tr" target="_blank" rel="noopener">orlex.com.tr &#8599;</a></li></ul></div>
      <div><h4>Export desk</h4><ul><li><a href="mailto:export@orlexglobal.com">export@orlexglobal.com</a></li><li><a href="tel:+905495011817">+90 549 501 18 17</a></li><li><a href="tel:+902125511869">+90 212 551 18 69</a></li><li>Yenibosna, Bahçelievler<br>Istanbul, Türkiye</li></ul></div>
    </div>
    <div class="bottom"><span>&copy; <span data-year>2026</span> Efamed Medical &middot; ORLEX is an Efamed brand</span><span>CE marked &middot; ISO 13485 &middot; UDI registered</span></div>
  </div>
</footer>
{sc}
</body>
</html>
'''

def phero(crumb, eyebrow, title, lede, actions=""):
    return f'''<section class="phero">
  {ARCS}
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a><span>/</span><span>{E(crumb)}</span></div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {actions}
  </div>
</section>
'''

def cta(title="Tell us your market. We’ll send the price list.", text="Distributors, importers, pharmacy and home-care chains: send your country and the product groups you work with. The export price list goes out the same week.", btn="Start an enquiry"):
    return f'''<section class="band tight"><div class="wrap"><div class="cta" data-reveal>
  {ARCS}
  <div><h2>{title}</h2><p>{text}</p></div>
  <div><a class="btn" href="contact.html" data-magnetic>{btn} <span class="arr">&rarr;</span></a></div>
</div></div></section>
'''

def card(icon, title, text, more=""):
    return f'<article class="card" data-reveal><div class="ico">{ICON[icon]}</div><h3>{title}</h3><p>{text}</p>{more}</article>'

# ---------- shared widgets ----------
def bodymap(link="products.html", start="knee", heading=True):
    head_html = f'''<div class="sec-head" data-reveal><div><span class="eyebrow">Product finder</span><h2>Start from the body, not the catalogue.</h2><p class="lede">Tap a region to see the ORLEX product groups that support it. Switch to the back view, or show children’s products only.</p></div></div>''' if heading else ""
    return f'''{head_html}
<div class="bodymap" data-bodymap data-link="{link}" data-start="{start}">
  <div class="figure-card" data-reveal>
    <div class="fig-bar">
      <div class="seg" role="group" aria-label="View"><button type="button" data-view="front" class="on" aria-pressed="true">Front</button><button type="button" data-view="back" aria-pressed="false">Back</button></div>
      <label class="kids"><input type="checkbox"> Children’s products only</label>
    </div>
    <div class="figure"><svg viewBox="0 0 600 1000" role="group" aria-label="Body map: choose a region"></svg></div>
  </div>
  <div data-reveal style="--d:.1s">
    <div class="panel" aria-live="polite"></div>
    <div class="region-pills"></div>
  </div>
</div>'''

def timeline(steps, dark=False):
    s = "".join(f'<div class="step"><h4>{t}</h4><p>{p}</p></div>' for t, p in steps)
    return f'<div class="timeline"><div class="fill"></div>{s}</div>'

FIRST_ORDER = [
  ("Enquiry", "Tell us your market, channel and the product groups you sell."),
  ("Price list & matching", "We send the export price list and map your list to ORLEX codes, line by line."),
  ("Samples", "Pick the codes. Samples go out at list price plus courier."),
  ("Proforma", "Quantities, sizes, packing and Incoterm confirmed on a proforma invoice."),
  ("Payment & production", "First order on 100% advance T/T. Production starts on receipt."),
  ("Shipment", "Goods leave Istanbul with full export documents and UDI-labelled packs."),
]

def orbit():
    sats = [("knee-supports","Knee",19),("corsets","Spine",29),("hand-wrist-finger-splints","Wrist & hand",27),("ankle-support-orthosis","Ankle",17),("neck-collars","Neck",11),("pediatric-products","Pediatric",22)]
    s = "".join(f'<a class="sat" href="products.html#{gid}"><i></i>{t} <small>{n}</small></a>' for gid, t, n in sats)
    return f'''<div class="orbit-wrap" data-reveal>
  <div class="orbit"><svg viewBox="0 0 500 500" aria-hidden="true">
    <g class="spin"><circle class="ring dash" cx="250" cy="250" r="232"/></g>
    <circle class="ring" cx="250" cy="250" r="190"/>
    <g class="spin rev"><circle class="ring dash" cx="250" cy="250" r="150"/></g>
    <g class="core"><image class="mark" href="assets/img/orlex-mark-512.png" x="138" y="138" width="224" height="224"/>    </g>
  </svg></div>
  {s}
</div>'''

def route():
    nodes = [(60,"Our facility","Istanbul"),(300,"Istanbul port","Loaded on board"),(540,"Your port","Destination"),(780,"Your warehouse","Named place")]
    n = "".join(f'<g class="node"><circle cx="{x}" cy="90" r="13"/><text x="{x}" y="132">{t}</text><text class="sub" x="{x}" y="152">{s}</text></g>' for x, t, s in nodes)
    return f'''<div class="route" id="route" data-reveal>
  <div class="terms-tabs" role="tablist" aria-label="Incoterms">
    <button type="button" data-t="EXW">EXW</button><button type="button" data-t="FOB">FOB</button><button type="button" data-t="CIF">CIF</button><button type="button" data-t="DAP">DAP</button><button type="button" data-t="DDP" class="off">DDP</button>
  </div>
  <svg viewBox="0 0 840 170" role="img" aria-label="Who handles each leg of the shipment">
    <path class="track" d="M60 90 C 180 40, 220 140, 300 90 S 460 30, 540 90 S 700 140, 780 90"/>
    <path class="seller" d="M60 90 C 180 40, 220 140, 300 90 S 460 30, 540 90 S 700 140, 780 90"/>
    {n}
    <g class="ship"><circle r="7" fill="#0D3981"/><circle r="3" fill="#fff"/></g>
  </svg>
  <div class="legend"><span><i></i>Handled by ORLEX</span><span><i class="b"></i>Handled by you / your forwarder</span></div>
  <div class="term-copy"><b>FOB</b><p></p></div>
</div>'''

# ---------- pages ----------
def page_index():
    jsonld = {"@context":"https://schema.org","@type":"Organization","name":"ORLEX","legalName":"Efamed Medical","url":SITE,"logo":SITE+"/assets/img/orlex-mark-512.png","foundingDate":"1993","email":"export@orlexglobal.com","telephone":"+90 549 501 18 17","address":{"@type":"PostalAddress","addressLocality":"Istanbul","addressCountry":"TR"},"sameAs":["https://www.orlex.com.tr"]}
    extra = '<script type="application/ld+json">' + json.dumps(jsonld) + '</script>\n'
    out = head("index.html", "ORLEX — Orthopaedic Supports Manufacturer, Istanbul", "ORLEX manufactures orthopaedic supports, braces and orthoses in Istanbul since 1993. 300+ references, CE marked, ISO 13485. Export price list for distributors.", extra)
    out += header("index.html")
    out += f'''<section class="hero">
  <div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div>
      <span class="eyebrow">Manufacturer &middot; Istanbul &middot; Since 1993</span>
      <h1 data-split>We make orthopaedic supports. <span class="accent">Not import them.</span></h1>
      <p class="lede" data-reveal>Braces, supports and orthoses from our own production in Istanbul, shipped to distributors in more than 40 countries. Over 300 references, CE marked and UDI registered &mdash; and we are looking for partners in new markets.</p>
      <div class="hero-actions" data-reveal style="--d:.15s">
        <a class="btn" href="contact.html" data-magnetic>Request the export price list <span class="arr">&rarr;</span></a>
        <a class="btn ghost" href="products.html">Explore the range</a>
      </div>
      <div class="hero-note" data-reveal style="--d:.25s"><span>CE marked</span><span>ISO 13485</span><span>UDI on every pack</span><span>Private label</span></div>
    </div>
    {orbit()}
  </div>
</section>
<section class="stats" aria-label="Key figures"><div class="wrap">
  <div class="stat"><b><span data-count="1993" data-from="1960">1993</span></b><span>Manufacturing since</span></div>
  <div class="stat"><b><span data-count="40">40</span><span class="u">+</span></b><span>Export countries</span></div>
  <div class="stat"><b><span data-count="300">300</span><span class="u">+</span></b><span>Product references</span></div>
  <div class="stat"><b><span data-count="{len(GROUPS)}">{len(GROUPS)}</span></b><span>Product groups</span></div>
  <div class="stat"><b><span data-count="9">9</span></b><span>IFU languages</span></div>
</div></section>
<div class="marquee" aria-hidden="true"><div class="track-m">{"".join("<span>"+t+"</span>" for t in ["Knee supports","Lumbosacral corsets","Cervical collars","Wrist & thumb splints","Ankle orthoses","Post-operative braces","Pediatric line","Compression stockings","Private label","UDI labelling"]*2)}</div></div>
<section class="band tint"><div class="wrap">{bodymap()}</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Why distributors choose ORLEX</span><h2>A manufacturer you can actually build a range on.</h2></div><a class="link" href="manufacturing.html">How we make it &rarr;</a></div>
  <div class="cards">
    {card("factory","Own production","Every reference is made in our facility in Istanbul. No trading layer between you and the line &mdash; and room to adjust specs and packing.",'<a class="link more" href="manufacturing.html">Manufacturing &rarr;</a>')}
    {card("doc","Documents ready","CE marking, ISO 13485 / 9001 / 14001 / 45001, UDI-DI and GTIN per reference, IFUs in nine languages. Ready before you ask.",'<a class="link more" href="certificates.html">Certificates &rarr;</a>')}
    {card("tag","Your brand","Private label on product, box, label and IFU. We keep the regulatory side straight while the brand is yours.",'<a class="link more" href="private-label.html">Private label &rarr;</a>')}
    {card("hand","Clear terms","Export price list ex-works Istanbul in USD and EUR. FOB, CIF or DAP quoted per shipment. No surprises at the proforma.",'<a class="link more" href="distributors.html">Trade terms &rarr;</a>')}
  </div>
</div></section>
<section class="band dark"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">From first email to first container</span><h2>Six steps to your first order.</h2></div><a class="btn ghost" href="distributors.html">Distributor terms</a></div>
  {timeline(FIRST_ORDER)}
</div></section>
{cta()}'''
    out += footer(DATA)
    return out

def page_products():
    out = head("products.html", "Product range — ORLEX orthopaedic supports", f"Browse {len(GROUPS)} ORLEX product groups and {NREFS} references: neck collars, corsets, knee, ankle, wrist and pediatric supports. Search by code and build your enquiry list.")
    out += header("products.html")
    out += phero("Products", "Product range", f"{len(GROUPS)} groups. Every code, searchable.", f"Search any reference by code or name, filter by body area, and add codes to your enquiry list. The full export price list with all 314 codes and sizes is sent on request.",
                 '<div class="hero-actions"><a class="btn" href="#explorer" data-magnetic>Search the range <span class="arr">&darr;</span></a><a class="btn ghost" href="https://www.orlex.com.tr/en/" target="_blank" rel="noopener">Photos on orlex.com.tr &#8599;</a></div>')
    out += f'''<section class="band tight tint"><div class="wrap">{bodymap(link="", start="knee")}</div></section>
<section id="explorer" class="tint" style="padding-bottom:100px">
  <div class="explorer-bar"><div class="wrap">
    <label class="search"><span class="sr">Search references</span><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search by code or name &mdash; e.g. DZ 13, lumbar, thumb" autocomplete="off"></label>
    <div class="filters" role="group" aria-label="Filter by group"></div>
  </div></div>
  <div class="wrap">
    <p class="result-line" aria-live="polite"></p>
    <div class="groups"></div>
    <div class="empty" hidden><h3>No reference matches that search.</h3><p>Try a code prefix like <b>DZ</b>, <b>K 5</b> or <b>A 7</b> &mdash; or <a class="link" href="contact.html">ask us directly</a>. We map customer lists to ORLEX codes line by line.</p></div>
  </div>
</section>
{cta("Picked your codes?","Your enquiry list travels with you to the contact page. Send it and we reply with prices, sizes and packing for exactly those references.","Review my enquiry")}'''
    out += footer(DATA)
    return out

def page_manufacturing():
    out = head("manufacturing.html", "Manufacturing & quality — ORLEX, Istanbul", "ORLEX orthopaedic supports are made in our own facility in Istanbul since 1993, under ISO 13485, ISO 9001, ISO 14001 and ISO 45001 management systems.")
    out += header("manufacturing.html")
    out += phero("Manufacturing", "Manufacturing & quality", "Made on our own lines in Istanbul.", "Efamed Medical has produced orthopaedic supports in Istanbul since 1993. Design, cutting, assembly, inspection and labelling happen under one roof &mdash; which is why we can change a size ladder, a packing unit or a label for you.")
    steps = [("Pattern & sizing","Anatomical patterns and full size ladders, from pediatric to XXL."),("Materials","Neoprene, knitted elastics, breathable fabrics, thermoplastics, aluminium and steel stays."),("Cutting","Material cut to pattern for each size and side."),("Sewing & assembly","Seams, straps, stays and fastenings assembled on our lines."),("Inspection","Finished products checked before packing, under our ISO 13485 system."),("UDI labelling & packing","Each pack labelled with UDI-DI / GTIN and a QR code to its product page.")]
    out += f'''<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Process</span><h2>From pattern to labelled pack.</h2></div></div>
  {timeline(steps)}
</div></section>
<section class="band tint"><div class="wrap split">
  <div data-reveal>
    <span class="eyebrow">Quality system</span>
    <h2 style="font-size:clamp(1.9rem,3.4vw,2.8rem);margin-top:16px">Certified, documented, traceable.</h2>
    <ul class="checks">
      <li>ISO 13485 quality management for medical devices</li>
      <li>ISO 9001, ISO 14001 and ISO 45001 alongside it</li>
      <li>CE marked range, Declaration of Conformity available on request</li>
      <li>UDI-DI and GTIN assigned to every reference</li>
      <li>Instructions for use printed in nine languages</li>
    </ul>
    <div class="hero-actions"><a class="btn" href="certificates.html" data-magnetic>See certificates <span class="arr">&rarr;</span></a></div>
  </div>
  <div class="plate draw" data-reveal style="--d:.1s"><svg viewBox="0 0 500 450" aria-hidden="true">
    <path d="M250 60a165 165 0 1 1-1 0" stroke="rgba(255,255,255,.12)" stroke-width="1.5" fill="none"/>
    <path d="M250 110a115 115 0 1 1-1 0" stroke="rgba(255,255,255,.18)" stroke-width="1.5" fill="none"/>
    <path d="M120 300a150 150 0 0 1 190-200" stroke="#EF7B00" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M380 150a150 150 0 0 1-190 200" stroke="#5B82C6" stroke-width="5" fill="none" stroke-linecap="round"/>
    <text x="250" y="232" text-anchor="middle" fill="#fff" font-size="54" font-weight="800" font-family="Manrope,sans-serif">1993</text>
    <text x="250" y="266" text-anchor="middle" fill="#A9B9D3" font-size="15" font-weight="700" letter-spacing="3" font-family="Manrope,sans-serif">ISTANBUL</text>
  </svg></div>
</div></section>
<section class="band"><div class="wrap">
  <div class="cards">
    {card("box","Packing your way","Unit packs, inner cartons and export cartons configured per market and per channel.")}
    {card("lang","Nine IFU languages","English, German, French, Italian, Romanian, Bulgarian, Greek, Russian and Turkish.")}
    {card("qr","QR on every label","Scan the code on a pack and it opens that exact product, size and lot on orlexglobal.com.")}
    {card("globe","40+ export markets","Running exports across Europe, the Middle East, Africa and beyond.")}
  </div>
</div></section>
{cta()}'''
    out += footer()
    return out

def page_private_label():
    out = head("private-label.html", "Private label & OEM orthopaedic supports — ORLEX", "Your brand on ORLEX orthopaedic supports: product, packaging, labels and instructions for use, manufactured in Istanbul.")
    out += header("private-label.html")
    out += phero("Private label", "Private label / OEM", "Your brand. Our factory.", "Put your name on product, box, label and IFU. We manufacture, label with UDI and keep the technical documentation in order &mdash; you build the brand in your market.")
    steps = [("Choose codes","Pick references from the range, or send your existing list to be matched."),("Samples","Standard samples at list price plus courier, to test fit and quality."),("Artwork","You send logo and colours; we prepare label, box and IFU layouts."),("Approval","You approve the proofs and the first production sample."),("Production","Manufactured and labelled in Istanbul, UDI on every pack."),("Repeat","Re-orders run on the approved artwork with no new set-up.")]
    out += f'''<section class="band"><div class="wrap split">
  <div data-reveal>
    <span class="eyebrow">Try it</span>
    <h2 style="font-size:clamp(1.9rem,3.4vw,2.8rem);margin-top:16px">See your name on the pack.</h2>
    <p class="lede" style="margin-top:16px">Type your brand and pick a colour. This is the kind of label we produce for partners &mdash; same product, your identity.</p>
    <ul class="checks">
      <li>Your brand on product, box, label and instructions for use</li>
      <li>Packaging languages and layout matched to your market</li>
      <li>Efamed Medical stays the legal manufacturer on the label, so the documentation stays valid</li>
      <li>Minimum quantities and set-up cost quoted per code</li>
      <li>We ship to your warehouse &mdash; we do not dropship to end customers</li>
    </ul>
  </div>
  <div data-reveal style="--d:.1s"><div class="label-demo">
    <div class="lb-top"><span class="lb-brand">YOUR BRAND</span><span class="lb-sw"><button type="button" class="on" data-c="#0D3981" style="background:#0D3981" aria-label="Navy"></button><button type="button" data-c="#0F7C6E" style="background:#0F7C6E" aria-label="Teal"></button><button type="button" data-c="#8A1C3F" style="background:#8A1C3F" aria-label="Burgundy"></button><button type="button" data-c="#1B2433" style="background:#1B2433" aria-label="Black"></button></span></div>
    <div class="rows"><div><span>Product</span><b>Knee support, patella</b></div><div><span>Size</span><b>M</b></div><div><span>Ref.</span><b>PL-DZ12-M</b></div><div><span>Lot</span><b>0127DZ12M1</b></div><div><span>Manufacturer</span><b>Efamed Medical, Istanbul</b></div></div>
    <div class="bars" aria-hidden="true"></div>
    <span class="ce" aria-hidden="true">CE</span>
    <label class="sr" for="brandin">Your brand name</label><input id="brandin" type="text" placeholder="Type your brand name" maxlength="22" autocomplete="off">
  </div></div>
</div></section>
<section class="band dark"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">How it runs</span><h2>From sample to your own range.</h2></div></div>
  {timeline(steps)}
</div></section>
{cta("Planning your own brand?","Send the product groups and rough volumes per model. We reply with MOQ, customisation cost and lead time per code.","Discuss private label")}'''
    out += footer()
    return out

def page_distributors():
    out = head("distributors.html", "Become an ORLEX distributor — trade terms", "Trade terms for ORLEX distributors: export price list ex-works Istanbul in USD and EUR, FOB, CIF or DAP shipping, samples, private label and exclusivity.")
    out += header("distributors.html")
    out += phero("Distributors", "Become a distributor", "Straight terms, stated up front.", "We work with importers, medical supply distributors, pharmacy and home-care chains and orthopaedic retailers. Here is exactly how working with us runs.",
                 '<div class="hero-actions"><a class="btn" href="contact.html" data-magnetic>Request the price list <span class="arr">&rarr;</span></a></div>')
    out += f'''<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Who we work with</span><h2>Partners who sell into the orthopaedic channel.</h2></div></div>
  <div class="cards">
    {card("box","Importers & distributors","Medical supply companies carrying supports and orthoses to hospitals, clinics and retail.")}
    {card("pharm","Pharmacy & home care","Chains and wholesalers serving pharmacies and home-care patients.")}
    {card("store","Orthopaedic retail","Orthopaedic and medical shops, Sanitätshaus and bandagist channels.")}
    {card("tender","Tenders","Partners bidding public tenders: we match tender lines to ORLEX codes and supply the documents.")}
  </div>
</div></section>
<section class="band tint"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Delivery terms</span><h2>Who handles which leg of the shipment.</h2><p class="lede">Pick an Incoterm to see where our responsibility ends and yours begins.</p></div></div>
  {route()}
</div></section>
<section class="band"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Trade terms</span><h2>The commercial basics.</h2></div></div>
  <dl class="terms" data-reveal>
    <div><dt>Price list</dt><dd>Ex-works Istanbul<small>USD and EUR, all references and sizes</small></dd></div>
    <div><dt>Shipping</dt><dd>FOB, CIF or DAP<small>Quoted per shipment. DDP is not offered.</small></dd></div>
    <div><dt>Payment</dt><dd>100% advance T/T on the first order<small>Terms reviewed as the relationship grows</small></dd></div>
    <div><dt>Samples</dt><dd>At list price plus courier<small>No mark-up on samples</small></dd></div>
    <div><dt>Private label</dt><dd>Available<small>MOQ and set-up quoted per code</small></dd></div>
    <div><dt>Exclusivity</dt><dd>Earned through performance<small>We start non-exclusive and discuss territory once volumes are there</small></dd></div>
    <div><dt>Lead time</dt><dd>Quoted per order<small>Driven by quantity and product group</small></dd></div>
    <div><dt>Matching</dt><dd>Line-by-line<small>Send your list or tender sheet &mdash; we map it to ORLEX codes</small></dd></div>
  </dl>
</div></section>
<section class="band dark"><div class="wrap">
  <div class="sec-head" data-reveal><div><span class="eyebrow">Your first order</span><h2>Six steps, no surprises.</h2></div></div>
  {timeline(FIRST_ORDER)}
</div></section>
{cta()}'''
    out += footer()
    return out

def seal(txt):
    return f'<div class="seal"><svg viewBox="0 0 74 74" aria-hidden="true"><circle class="r1" cx="37" cy="37" r="33"/><circle class="r2" cx="37" cy="37" r="27"/><text x="37" y="42">{txt}</text></svg></div>'

def page_certificates():
    sample = "01/08682132200019/10/0127B201S1/"
    out = head("certificates.html", "Certificates & compliance — ORLEX", "ORLEX compliance: CE marked range, ISO 13485, ISO 9001, ISO 14001 and ISO 45001 certified, UDI-DI and GTIN per reference, IFUs in nine languages.")
    out += header("certificates.html")
    out += phero("Certificates", "Compliance", "The paperwork is already done.", "Most of what slows a new supplier down is documentation. Ours is in place before you ask &mdash; and we send the full set with the price list.",
                 '<div class="hero-actions"><a class="btn" href="contact.html" data-magnetic>Request the document set <span class="arr">&rarr;</span></a></div>')
    certs = [("13485","ISO 13485","Quality management system for medical devices.","Certified"),("9001","ISO 9001","Quality management system.","Certified"),("14001","ISO 14001","Environmental management system.","Certified"),("45001","ISO 45001","Occupational health and safety management.","Certified"),
             ("CE","CE marking","The range is CE marked. Declaration of Conformity available on request.","On request"),("UDI","UDI","UDI-DI and GTIN assigned to every reference; EMDN and GMDN held per product group.","Every pack")]
    cc = "".join(f'<article class="cert" data-reveal>{seal(s)}<h3>{t}</h3><p>{p}</p><span class="tag">{g}</span></article>' for s, t, p, g in certs)
    out += f'''<section class="band"><div class="wrap">
  <div class="certs">{cc}</div>
</div></section>
<section class="band tint"><div class="wrap split">
  <div data-reveal>
    <span class="eyebrow">Traceability</span>
    <h2 style="font-size:clamp(1.9rem,3.4vw,2.8rem);margin-top:16px">Scan the pack. Open the product.</h2>
    <p class="lede" style="margin-top:16px">Every ORLEX label carries a GS1 QR code. Scanning it opens a page for that exact product, size and lot on orlexglobal.com &mdash; for pharmacists, distributors and patients alike.</p>
    <div class="hero-actions"><a class="btn ghost" href="{sample}">Open a sample label page &rarr;</a></div>
  </div>
  <div class="cards" data-reveal style="--d:.1s">
    {card("qr","GS1 Digital Link","Label QR codes follow the GS1 format: GTIN, then batch / lot.")}
    {card("lang","IFUs in nine languages","English, German, French, Italian, Romanian, Bulgarian, Greek, Russian, Turkish.")}
    {card("shield","Registration support","We supply the documentation set for local health-authority registration and work through it with your regulatory team.")}
  </div>
</div></section>
{cta("Need the documents for a tender or a registration?","Tell us the authority and the product lines. We send certificates, the Declaration of Conformity and the technical summaries you need.","Request documents")}'''
    out += footer()
    return out

def page_contact():
    out = head("contact.html", "Contact the ORLEX export desk", "Contact ORLEX export: export@orlexglobal.com, +90 549 501 18 17. Send your market and product groups and receive the export price list.")
    out += header("contact.html")
    out += phero("Contact", "Export desk", "Tell us your market.", "We answer within one working day. Send the codes you picked, or describe what you sell &mdash; we match it to the ORLEX range and send prices.")
    out += '''<section class="band"><div class="wrap contact-grid">
  <form id="enquiry" class="form" data-reveal novalidate>
    <div class="field"><label for="company">Company *</label><input id="company" name="company" required autocomplete="organization"></div>
    <div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name"></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
    <div class="field"><label for="country">Country / market *</label><input id="country" name="country" required autocomplete="country-name"></div>
    <div class="field full"><label for="type">Business type</label><select id="type" name="type"><option>Importer / distributor</option><option>Pharmacy or home-care chain</option><option>Orthopaedic retail</option><option>Tender / public procurement</option><option>Private label brand</option><option>Other</option></select></div>
    <div class="field full"><label>Products of interest</label><div id="picked" class="picked"></div></div>
    <div class="field full"><label for="message">Message</label><textarea id="message" name="message" placeholder="Product groups, rough quantities, target price, delivery terms&hellip;"></textarea></div>
    <div class="full" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><button class="btn" type="submit" data-magnetic>Send enquiry <span class="arr">&rarr;</span></button><span class="hint">Opens your email app with the enquiry ready to send to export@orlexglobal.com.</span></div>
  </form>
  <aside class="side" data-reveal style="--d:.1s">
    <div class="card"><h3>Export</h3><p><a href="mailto:export@orlexglobal.com">export@orlexglobal.com</a><br><a href="tel:+905495011817">+90 549 501 18 17</a> &middot; WhatsApp<br><a href="tel:+902125511869">+90 212 551 18 69</a></p></div>
    <div class="card"><h3>Factory</h3><p>Saçsan Sanayi Sitesi, Çardak Sok. No:16-15<br>Çobançeşme Mah., Yenibosna<br>Bahçelievler, Istanbul, Türkiye</p></div>
    <div class="card"><h3>Product photos & size charts</h3><p><a href="https://www.orlex.com.tr/en/" target="_blank" rel="noopener">orlex.com.tr &#8599;</a></p></div>
    <div class="card"><h3>Find us at</h3><p>MEDICA D&uuml;sseldorf &middot; Expomed Istanbul</p></div>
  </aside>
</div></section>
'''
    out += footer()
    return out

PAGES = {"index.html": page_index, "products.html": page_products, "manufacturing.html": page_manufacturing,
         "private-label.html": page_private_label, "distributors.html": page_distributors,
         "certificates.html": page_certificates, "contact.html": page_contact}

THUMBS = set(json.load(open(os.path.join(ROOT, "_build", "thumbs.json"), encoding="utf-8")))

def _thumb(code):
    import re as _re
    k = _re.sub(r"[^A-Z0-9Ç]", "", code.upper().replace("ORX", ""))
    return k if k in THUMBS else ""

def write_data():
    import re as _re
    out = []
    for x in GROUPS:
        slug = _re.sub(r"[^a-z0-9]+", "-", x["name"].lower()).strip("-")
        m = _re.match(r"ORX-([A-Z]+)", x["refs"][0]["c"])
        out.append({"id": slug, "name": x["name"], "desc": x["desc"], "cat": x["cat"], "prefix": m.group(1) if m else "ORX",
                    "url": x["url"], "refs": [[r["c"], r["n"], _thumb(r["c"])] for r in x["refs"]]})
    with open(os.path.join(ROOT, "assets", "js", "products-data.js"), "w", encoding="utf-8") as f:
        f.write("/* ORLEX product groups \u2014 generated by _build/gen.py from _build/groups.json */\nwindow.ORLEX_GROUPS=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")

if __name__ == "__main__":
    write_data()
    for name, fn in PAGES.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
