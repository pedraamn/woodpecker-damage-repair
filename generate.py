#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import html
import re
import shutil



from dataclasses import dataclass
from pathlib import Path
from datetime import date

@dataclass(frozen=True)
class SiteConfig:
  # Data
  cities_csv: Path = Path("cities.csv")

  def load_cities(self):
    return load_cities_from_csv(self.cities_csv)

  from pathlib import Path

  base_name: str = "Woodpecker Damage Repair"
  brand_name: str = "Woodpecker Damage Repair Company"
  cta_text: str = "Get Free Estimate"
  cta_href: str = "/contact/"

  # Build / assets
  output_dir: Path = Path("public")
  image_filename: str = "picture.png"  # sits next to generate.py

  # Pricing (base range; city pages may apply multipliers)
  cost_low: int = 350
  cost_high: int = 1500

  # Page H1 titles
  h1_title: str = "Woodpecker Damage Repair/Woodpecker Hole Repair/Siding Repair Services"
  h1_short: str = "Woodpecker Damage Repair Services"
  h1_sub: str = "Weather-tight siding and trim repairs that seal holes, match finishes, and reduce repeat damage."

  cost_title: str = "Woodpecker Damage Repair Cost"
  cost_sub: str = "Typical pricing ranges, scope examples, and what drives the total for siding and trim repairs."

  howto_title: str = "How Woodpecker Damage Repair Works"
  howto_sub: str = "A practical, homeowner-friendly guide to how repairs are typically done and when DIY breaks down."

  # MAIN PAGE (shared guide)
  main_h2: list[str] = (
    "What Is Woodpecker Damage Repair?",
    "Why Are Woodpeckers Pecking My House?",
    "What Do Woodpecker Holes Look Like in Siding or Trim?",
    "Is Woodpecker Damage Bad for Your House?",
    "Does Woodpecker Damage Mean Termites?",
    "Is Woodpecker Damage Covered by Insurance?",
    "When to Hire a Professional for Woodpecker Damage Repair",
  )

  main_p: list[str] = (
    "Woodpecker damage repair is the process of sealing and restoring holes in siding, trim, fascia, or soffits so the exterior is weather-tight again. The goal isn’t just to fill a hole—it’s to stabilize the surrounding material and restore a finish that won’t fail in the next storm.",
    "Woodpeckers usually peck homaes to search for insects, create a nesting cavity, or drum to mark territory. The reason matters because repairs last longer when you reduce what attracted the bird in the first place, instead of only patching the visible holes.",
    "Woodpecker holes often appear as clean round openings, clusters of small probing holes, or larger cavities where the bird returned repeatedly. The pattern helps identify whether the issue is light probing or more serious nesting damage that may require replacement instead of patching.",
    "Yes, woodpecker damage can be serious because even small holes can let water and pests into the wall system. Over time, repeated wetting can cause paint failure, swelling, rot, and bigger repairs than the original hole.",
    "Woodpecker activity doesn’t automatically mean termites, but it can signal insects in or around the wood. If you’re seeing soft wood, frass, or repeated pecking in one area, treat it as a ‘possible pest + repair’ situation so you don’t seal in a hidden problem.",
    "Insurance coverage for woodpecker damage depends on the policy and how the damage is classified. If you’re considering a claim, early photos and a repair assessment can help clarify what’s covered versus what’s considered maintenance or gradual wear.",
    "Hire a professional when damage is spread across multiple areas, the wood is soft or deteriorated, repairs require ladder work, or finish matching matters. Professional {woodpecker damage repair services} typically include proper sealing, material stabilization, and finish blending so the repair holds up and looks consistent.",
  )

  # HOW-TO PAGE (ordered, process-first; general guide vs step-by-step tutorial)
  howto_h2: list[str] = (
    "Quick Answer: How Does Woodpecker Damage Repair Usually Work?",
    "How Professionals Identify the Extent of Woodpecker Damage",
    "How Repair Methods Are Chosen for Woodpecker Holes",
    "How Woodpecker Damage Is Sealed Against Water",
    "How Finish Matching Affects the Final Repair",
    "When DIY Woodpecker Repairs Commonly Fail",
  )

  howto_p: list[str] = (
    "Woodpecker damage repair usually works by removing weak material, sealing the opening, patching or replacing the damaged section, and restoring the finish so it’s weather-tight again. Pros focus on moisture control and adhesion because a patch that looks fine today can fail quickly if water can get behind it.",
    "The first step is checking whether the damage is only in the siding/trim or if moisture has affected the material behind it. This matters because sealing a hole over soft wood or hidden rot leads to repeat failure and larger repair scope later.",
    "The repair method depends on hole size, hole density, and whether the surrounding wood is sound. Small, isolated holes may be patched on solid material, but repeated damage or weak edges often calls for replacing boards or trim so the repair has a stable base.",
    "A durable repair seals the hole and the repair edges so wind-driven rain can’t wick behind the finish. Many DIY repairs fail because the patch isn’t fully sealed, which allows moisture intrusion and breaks down adhesion over time.",
    "Finish matching is what makes repairs blend and stay durable, especially on stained or weathered exteriors. Even when the patch is structurally sound, mismatched paint, sheen, or texture can make the repair stand out and may require a larger blend area to look consistent.",
    "DIY repairs commonly fail when the underlying wood is soft, the repair isn’t fully sealed, or finish bonding is poor on weathered surfaces. If you want a realistic sense of pricing when repairs involve replacement and finish blending, you can {view our woodpecker damage repair cost guide}.",
  )

  # COST PAGE (your cost-guide vibe; no walkthroughs)
  cost_h2: list[str] = (
    "Quick Answer",
    "Direct Answer: How Much Does Woodpecker Damage Repair Cost?",
    "Woodpecker Damage Repair Cost by Scope",
    "Woodpecker Damage Repair Cost by Method",
    "What Affects Woodpecker Damage Repair Pricing?",
    "Related Cost Questions",
    "Expert Insight from an Exterior Repair Perspective",
    "Key Takeaways",
  )

  cost_p: list[str] = (
    "Woodpecker damage repair typically costs {cost_lo} to {cost_hi}, depending on how many holes there are, whether boards need replacement, and how much finish matching is required. Small patch-and-touch-up repairs are often cheaper, while scattered damage and repainting push costs higher.",
    "Most homeowners can expect to pay {cost_lo} to {cost_hi} for professional woodpecker damage repair, with the total driven by scope and finish work. Many contractors include a minimum service fee because setup, ladder work, and blending take time even on small repairs.",
    "Costs rise with the number of damaged areas and whether repairs are concentrated in one spot or spread across the exterior. A few holes in one board is usually faster than scattered damage across multiple elevations that requires repeated setup and blending.",
    "Patching can be cost-effective when surrounding wood is solid, while replacement is more common when damage is widespread or edges are weak. Finish matching (paint, stain, or texture) is often the biggest price multiplier because blending may require repainting a larger section than the hole itself.",
    "The biggest pricing drivers are repair count, access height, substrate condition, and finish matching requirements. If moisture has affected the material behind the siding, scope increases because the repair becomes a sealing and restoration job rather than cosmetic filling.",
    "Is it cheaper to repair woodpecker holes yourself? DIY can cost less in materials, but failures from poor sealing or weak wood often create higher repair costs later. What does it cost to fix woodpecker damage to siding? Siding repairs range widely based on patching versus replacing boards and repainting to blend.",
    "The most expensive woodpecker repairs are usually the ones done twice. A repair that isn’t fully sealed—or that’s installed on soft wood—can reopen quickly and allow moisture intrusion, expanding the scope. That’s why many homeowners choose {expert woodpecker damage repair services} when durability and finish quality matter.",
    "Woodpecker damage repair typically costs {cost_lo} to {cost_hi}. Replacement and finish blending are what most often increase total cost. Access height and scattered damage add labor time fast. Pairing repair with deterrence reduces the odds you pay twice.",
  )

  # LOCAL COST (city-locked variant)
  location_cost_h2: str = "How Much Does Woodpecker Damage Repair Cost in {City, State}?"

  location_cost_p: str = (
    "In {City, State}, most woodpecker damage repair projects range from {cost_lo} to {cost_hi}, "
    "depending on scope and access difficulty. Prices can vary based on local labor rates, property layout, and finish matching requirements. "
    "For a clearer breakdown of what affects pricing, you can {view our woodpecker damage repair cost guide}."
  )

  # IMAGES
  image_prompt: str = (
    "A realistic natural-light photo of a home exterior repair in progress: a real human contractor on a ladder "
    "repairing small round woodpecker holes in painted wood siding near trim on a suburban house. "
    "The worker wears safety glasses and gloves, using a putty knife and exterior-grade patch compound and a caulk gun; "
    "tools visible, non-staged candid feel, residential yard background."
  )





CONFIG = SiteConfig()

CityWithCol = tuple[str, str, float]

def load_cities_from_csv(path: Path) -> tuple[CityWithCol, ...]:
  cities: list[CityWithCol] = []

  with path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    required_fields = {"city", "state", "col"}
    if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
      raise ValueError(
          "CSV must have headers: city,state,col "
          f"(found: {reader.fieldnames})"
      )

    for i, row in enumerate(reader, start=2):  # header is line 1
      city = (row.get("city") or "").strip()
      state = (row.get("state") or "").strip().upper()
      col_raw = (row.get("col") or "").strip()

      if not city or not state or not col_raw:
        raise ValueError(f"Missing city/state/col at CSV line {i}: {row}")

      try:
        col = float(col_raw)
      except ValueError as e:
        raise ValueError(
            f"Invalid col value at CSV line {i}: {col_raw!r}"
        ) from e

      cities.append((city, state, col))

  return tuple(cities)

CITIES: tuple[CityWithCol, ...] = CONFIG.load_cities()



"""
ALSO_MENTIONED = [
    "pest control",
    "spray",
    "spray bottle",
    "dish soap",
    "wasp stings",
    "price",
    "removal",
    "nest",
    "wasp",
]
"""


# -----------------------
# HELPERS
# -----------------------
def esc(s: str) -> str:
    return html.escape(s, quote=True)


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def city_state_slug(city: str, state: str) -> str:
    return f"{slugify(city)}-{slugify(state)}"


def clamp_title(title: str, max_chars: int = 70) -> str:
    if len(title) <= max_chars:
        return title
    return title[: max_chars - 1].rstrip() + "…"


def city_title(city: str, state: str) -> str:
    return clamp_title(f"{CONFIG.h1_short} in {city}, {state}", 70)


def write_text(out_path: Path, content: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")


def reset_output_dir(p: Path) -> None:
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)


def copy_site_image(*, src_dir: Path, out_dir: Path, filename: str) -> None:
    src = src_dir / filename
    if not src.exists():
        raise FileNotFoundError(f"Missing image next to generate.py: {src}")
    shutil.copyfile(src, out_dir / filename)


# -----------------------
# THEME (pure CSS, minimal, fast)
# Home-services vibe: warmer neutrals + trustworthy green CTA.
# -----------------------
CSS = """
:root{
  --bg:#fafaf9;
  --surface:#ffffff;
  --ink:#111827;
  --muted:#4b5563;
  --line:#e7e5e4;
  --soft:#f5f5f4;

  --cta:#16a34a;
  --cta2:#15803d;

  --max:980px;
  --radius:16px;
  --shadow:0 10px 30px rgba(17,24,39,0.06);
  --shadow2:0 10px 24px rgba(17,24,39,0.08);
}
*{box-sizing:border-box}
html{color-scheme:light}
body{
  margin:0;
  font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
  color:var(--ink);
  background:var(--bg);
  line-height:1.6;
}
a{color:inherit}
a:focus{outline:2px solid var(--cta); outline-offset:2px}

/* -----------------------
   TOP NAV
----------------------- */
.topbar{
  position:sticky;
  top:0;
  z-index:50;
  background:rgba(250,250,249,0.92);
  backdrop-filter:saturate(140%) blur(10px);
  border-bottom:1px solid var(--line);
}
.topbar-inner{
  max-width:var(--max);
  margin:0 auto;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:14px;
}
.brand{
  font-weight:900;
  letter-spacing:-0.02em;
  text-decoration:none;
}
.nav{
  display:flex;
  align-items:center;
  gap:12px;
  flex-wrap:wrap;
  justify-content:flex-end;
}
.nav a{
  text-decoration:none;
  font-size:13px;
  color:var(--muted);
  padding:7px 10px;
  border-radius:12px;
  border:1px solid transparent;
}
.nav a:hover{
  background:var(--soft);
  border-color:var(--line);
}
.nav a[aria-current="page"]{
  color:var(--ink);
  background:var(--soft);
  border:1px solid var(--line);
}

/* CTA button */
.btn{
  display:inline-block;
  padding:9px 12px;
  background:var(--cta);
  color:#fff;
  border-radius:12px;
  text-decoration:none;
  font-weight:900;
  font-size:13px;
  border:1px solid rgba(0,0,0,0.04);
  box-shadow:0 8px 18px rgba(22,163,74,0.18);
}
.btn:hover{background:var(--cta2)}
.btn:focus{outline:2px solid var(--cta2); outline-offset:2px}

/* Keep CTA white in nav */
.nav a.btn{
  color:#fff;
  background:var(--cta);
  border-color:rgba(0,0,0,0.04);
}
.nav a.btn:hover{background:var(--cta2)}

/* -----------------------
   HERO
----------------------- */
header{
  border-bottom:1px solid var(--line);
  background:
    radial-gradient(1200px 380px at 10% -20%, rgba(22,163,74,0.08), transparent 55%),
    radial-gradient(900px 320px at 95% -25%, rgba(17,24,39,0.06), transparent 50%),
    #fbfbfa;
}
.hero{
  max-width:var(--max);
  margin:0 auto;
  padding:34px 18px 24px;
  display:grid;
  gap:10px;
}
.hero h1{
  margin:0;
  font-size:30px;
  letter-spacing:-0.03em;
  line-height:1.18;
}
.sub{
  margin:0;
  color:var(--muted);
  max-width:78ch;
  font-size:14px;
}

/* -----------------------
   MAIN CONTENT
----------------------- */
main{
  max-width:var(--max);
  margin:0 auto;
  padding:22px 18px 46px;
}
.card{
  background:var(--surface);
  border:1px solid var(--line);
  border-radius:var(--radius);
  padding:18px;
  box-shadow:var(--shadow);
}

/* Service image – responsive, smaller on desktop */
.img{
  margin-top:14px;
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--line);
  background:var(--soft);
  box-shadow:var(--shadow2);
  width:100%;
}
.img img{
  display:block;
  width:100%;
  height:auto;
}

/* ~50% width on desktop */
@media (min-width: 900px){
  .img{
    max-width:50%;
    margin-left:auto;
    margin-right:auto;
  }
}

h2{
  margin:18px 0 8px;
  font-size:16px;
  letter-spacing:-0.01em;
}
p{margin:0 0 10px}
.muted{color:var(--muted); font-size:13px}
hr{border:0; border-top:1px solid var(--line); margin:18px 0}

/* -----------------------
   CITY GRID
----------------------- */
.city-grid{
  list-style:none;
  padding:0;
  margin:10px 0 0;
  display:grid;
  gap:10px;
  grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
}
.city-grid a{
  display:block;
  text-decoration:none;
  color:var(--ink);
  background:#fff;
  border:1px solid var(--line);
  border-radius:14px;
  padding:12px;
  font-weight:800;
  font-size:14px;
  box-shadow:0 10px 24px rgba(17,24,39,0.05);
}
.city-grid a:hover{
  transform:translateY(-1px);
  box-shadow:0 14px 28px rgba(17,24,39,0.08);
}

/* -----------------------
   CALLOUT
----------------------- */
.callout{
  margin:16px 0 12px;
  padding:14px;
  border-radius:14px;
  border:1px solid rgba(22,163,74,0.22);
  background:linear-gradient(180deg, rgba(22,163,74,0.08), rgba(22,163,74,0.03));
}
.callout-title{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:900;
}
.badge{
  padding:3px 10px;
  border-radius:999px;
  background:rgba(22,163,74,0.14);
  border:1px solid rgba(22,163,74,0.22);
  font-size:12px;
  font-weight:900;
}

/* -----------------------
   CONTACT FORM (UPDATED)
----------------------- */
.form-grid{
  margin-top:14px;
  display:grid;
  gap:14px;
  grid-template-columns:1fr 320px;
  align-items:start;
}
@media (max-width: 900px){
  .form-grid{grid-template-columns:1fr}
}

.embed-card{
  border:1px solid var(--line);
  border-radius:14px;
  padding:18px;
  background:var(--soft);
}

.nx-center{
  display:flex;
  justify-content:center; /* mobile centered */
}

/* Networx container sizing (mobile-first) */
#nx_form{
  width:100%;
  max-width:520px;
  min-height:520px;
}

/* Force iframe to fill container */
#networx_form_container iframe{
  width:100% !important;
  height:100% !important;
  border:0 !important;
}


/* -----------------------
   WHY BOX
----------------------- */
.why-box{
  background:#fff;
  border:1px solid var(--line);
  border-radius:14px;
  padding:14px;
  box-shadow:0 10px 24px rgba(17,24,39,0.05);
}
.why-box h3{
  margin:0 0 10px;
  font-size:15px;
}
.why-list{
  list-style:none;
  padding:0;
  margin:0;
  display:grid;
  gap:10px;
}
.why-item{
  display:flex;
  gap:10px;
  align-items:flex-start;
  color:var(--muted);
  font-size:13px;
}
.tick{
  width:18px;
  height:18px;
  border-radius:999px;
  background:rgba(22,163,74,0.12);
  border:1px solid rgba(22,163,74,0.22);
  display:inline-flex;
  align-items:center;
  justify-content:center;
}
.tick:before{
  content:"✓";
  font-weight:900;
  font-size:12px;
}

/* -----------------------
   FOOTER
----------------------- */
footer{
  border-top:1px solid var(--line);
  background:#fbfbfa;
}
.footer-inner{
  max-width:var(--max);
  margin:0 auto;
  padding:28px 18px;
  display:grid;
  gap:10px;
}
.footer-links{
  display:flex;
  gap:12px;
  flex-wrap:wrap;
}
.footer-links a{
  color:var(--muted);
  text-decoration:none;
  font-size:13px;
}
.small{
  color:var(--muted);
  font-size:12px;
}

/* -----------------------
   MOBILE NAV FIX (KEY PART)
----------------------- */
@media (max-width: 640px){
  .topbar-inner{
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .nav{
    justify-content: center;
  }

  .nav .btn{
    width: 100%;
    text-align: center;
  }
}
""".strip()




# -----------------------
# HTML BUILDING BLOCKS
# -----------------------
def nav_html(current: str) -> str:
    def item(href: str, label: str, key: str) -> str:
        cur = ' aria-current="page"' if current == key else ""
        return f'<a href="{esc(href)}"{cur}>{esc(label)}</a>'

    return (
        '<nav class="nav" aria-label="Primary navigation">'
        + item("/", "Home", "home")
        + item("/cost/", "Cost", "cost")
        + item("/how-to/", "How-To", "howto")
        + f'<a class="btn" href="{esc(CONFIG.cta_href)}">{esc(CONFIG.cta_text)}</a>'
        + "</nav>"
    )


def base_html(*, title: str, canonical_path: str, current_nav: str, body: str) -> str:
    # title == h1 is enforced by callers; keep this thin.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <link rel="canonical" href="{esc(canonical_path)}" />
  <style>
{CSS}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="/">{esc(CONFIG.brand_name)}</a>
      {nav_html(current_nav)}
    </div>
  </div>
{body}
</body>
</html>
"""


def header_block(*, h1: str, sub: str) -> str:
    return f"""
<header>
  <div class="hero">
    <h1>{esc(h1)}</h1>
    <p class="sub">{esc(sub)}</p>
  </div>
</header>
""".rstrip()

def contact_header_block(*, h1: str, sub: str) -> str:
    return f"""
<header class="contact-hero">
  <div class="hero">
    <h1>{esc(h1)}</h1>
    <p class="sub">{esc(sub)}</p>
  </div>
</header>
""".rstrip()


def footer_block(*, show_cta: bool = True) -> str:
    cta_html = ""
    if show_cta:
        cta_html = f"""
    <h2>Next steps</h2>
    <p class="sub">Ready to move forward? Request a free quote.</p>
    <div>
      <a class="btn" href="{esc(CONFIG.cta_href)}">{esc(CONFIG.cta_text)}</a>
    </div>
"""

    return f"""
<footer>
  <div class="footer-inner">
    {cta_html}
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/cost/">Cost</a>
      <a href="/how-to/">How-To</a>
    </div>
    <div class="small">© {esc(CONFIG.brand_name)}. All rights reserved.</div>
  </div>
</footer>
""".rstrip()



def page_shell(*, h1: str, sub: str, inner_html: str, show_image: bool = True, show_footer_cta: bool = True) -> str:
    img_src = f"/{CONFIG.image_filename}"
    img_html = ""
    if show_image:
        img_html = f"""
    <div class="img">
      <img src="{esc(img_src)}" alt="Service image" loading="lazy" />
    </div>
""".rstrip()

    return (
        header_block(h1=h1, sub=sub)
        + f"""
<main>
  <section class="card">
{img_html}
    {inner_html}
  </section>
</main>
"""
        + footer_block(show_cta=show_footer_cta)
    ).rstrip()



# -----------------------
# CONTENT SECTIONS
# -----------------------

def linkify_curly(text: str) -> str:
  """
  Replace {word} with a link to the homepage using that word as link text
  """
  parts = []
  last = 0

  for m in re.finditer(r"\{([^}]+)\}", text):
    # text before the match
    parts.append(esc(text[last:m.start()]))

    word = m.group(1)
    parts.append(f'<a href="/">{esc(word)}</a>')

    last = m.end()

  # remaining text
  parts.append(esc(text[last:]))

  return "".join(parts)

def make_section(*, headings: list[str], paras:  list[str]) -> str:
  parts = []
  for h2, p in zip(headings, paras):
    parts.append(f"<h2>{esc(h2)}</h2>")
    parts.append(f"<p>{linkify_curly(p)}</p>")
  return "\n".join(parts)

def location_cost_section(city: str, state: str, col: float) -> str:
    cost_lo = f"<strong>${int(CONFIG.cost_low * col)}</strong>"
    cost_hi = f"<strong>${int(CONFIG.cost_high * col)}</strong>"

    h2 = CONFIG.location_cost_h2.replace(
        "{City, State}", f"{city}, {state}"
    )

    p = (
        CONFIG.location_cost_p
        .replace("<strong>{City, State}", f"{city}, {state}</strong>")
        .replace("{cost_lo}", cost_lo)
        .replace("{cost_hi}", cost_hi)
    )

    return f"<h2>{esc(h2)}</h2>\n<p>{esc(p)}</p>"


def city_cost_callout_html(city: str, state: str) -> str:
    # Subtle, high-impact conversion element for city pages.
    return f"""
<div class="callout" role="note" aria-label="Typical cost range">
  <div class="callout-title">
    <span class="badge">Typical range in {esc(city)}, {esc(state)}</span>
    <span>${CONFIG.cost_low}–${CONFIG.cost_high}</span>
  </div>
</div>
""".rstrip()


# -----------------------
# PAGE FACTORY
# -----------------------
def make_page(*, h1: str, canonical: str, nav_key: str, sub: str, inner: str, show_image: bool = True, show_footer_cta: bool = True) -> str:
    h1 = clamp_title(h1, 70)
    title = h1  # enforce title == h1
    return base_html(
        title=title,
        canonical_path=canonical,
        current_nav=nav_key,
        body=page_shell(h1=h1, sub=sub, inner_html=inner, show_image=show_image, show_footer_cta=show_footer_cta),
    )


def homepage_html() -> str:
    city_links = "\n".join(
        f'<li><a href="{esc("/" + city_state_slug(city, state) + "/")}">{esc(city)}, {esc(state)}</a></li>'
        for city, state, _ in CITIES
    )
    inner = (
        make_section(headings=CONFIG.main_h2, paras=CONFIG.main_p)
        + """
<hr />
<h2>Choose your city</h2>
<p class="muted">We provide services nationwide, including in the following cities:</p>
<ul class="city-grid">
"""
        + city_links
        + f"""
</ul>
<hr />
<p class="muted">
  Also available: <a href="/cost/">{esc(CONFIG.cost_title)}</a> and <a href="/how-to/">{esc(CONFIG.howto_title)}</a>.
</p>
"""
    )

    return make_page(
        h1=CONFIG.h1_title,
        canonical="/",
        nav_key="home",
        sub=CONFIG.h1_sub,
        inner=inner,
    )

def contact_page_html() -> str:
    # Hard-coded copy
    h1 = "Get Your Free Estimate"
    sub = "Fill out the form below and we'll connect you with a qualified local professional."

    why_title = "Why Choose Us?"
    why_bullets = (
        "Free, no-obligation estimates",
        "Trusted, experienced professionals",
        "Nationwide service coverage",
        "Fast response times",
    )

    why_items = "\n".join(
        f'<li class="why-item"><span class="tick" aria-hidden="true"></span><span>{esc(t)}</span></li>'
        for t in why_bullets
    )

    # ✅ Paste your Networx embed EXACTLY here.
    # (This is the snippet style from your screenshot.)
    networx_embed = """
<div id="networx_form_container" style="margin:0px;padding:0px;">
    <div id = "nx_form" style = "width: 242px; height: 375px;">
        <script type="text/javascript" src = "https://api.networx.com/iframe.php?aff_id=73601bc3bd5a961a61a973e92e29f169&aff_to_form_id=7994"></script>
    </div>
</div>
""".strip()

    inner = f"""
<div class="form-grid">
  <div class="embed-card">
    <div class="nx-center">
      {networx_embed}
    </div>
  </div>

  <aside class="why-box" aria-label="Why choose us">
    <h3>{esc(why_title)}</h3>
    <ul class="why-list">
      {why_items}
    </ul>
  </aside>
</div>
""".strip()

    # Use the same site shell, but NO image on contact (recommended)
    return make_page(
        h1=h1,
        canonical="/contact/",
        nav_key="contact",
        sub=sub,
        inner=inner,
        show_image=False,
        show_footer_cta=False
    )



def city_page_html(city: str, state: str, col: float) -> str:
    inner = (
      location_cost_section(city, state, col)
      + make_section(headings=CONFIG.main_h2, paras=CONFIG.main_p)
    )

    return make_page(
        h1=city_title(city, state),
        canonical=f"/{city_state_slug(city, state)}/",
        nav_key="home",
        sub=CONFIG.h1_sub,
        inner=inner,
    )


def cost_page_html() -> str:
    return make_page(
        h1=CONFIG.cost_title,
        canonical="/cost/",
        nav_key="cost",
        sub=CONFIG.cost_sub,
        inner=make_section(headings=CONFIG.cost_h2, paras=CONFIG.cost_p),
    )


def howto_page_html() -> str:
    return make_page(
        h1=CONFIG.howto_title,
        canonical="/how-to/",
        nav_key="howto",
        sub=CONFIG.howto_sub,
        inner=make_section(headings=CONFIG.howto_h2, paras=CONFIG.howto_p),
    )


# -----------------------
# ROBOTS + SITEMAP + WRANGLER
# -----------------------
def robots_txt() -> str:
    return "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"


def sitemap_xml(urls: list[str]) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
        + "</urlset>\n"
    )

def wrangler_content() -> str:
    name = CONFIG.base_name.lower().replace(" ", "-")
    today = date.today().isoformat()

    return f"""{{
  "name": "{name}",
  "compatibility_date": "{today}",
  "assets": {{
    "directory": "./public"
  }}
}}
"""


# -----------------------
# MAIN
# -----------------------
def main() -> None:
  script_dir = Path(__file__).resolve().parent
  out = CONFIG.output_dir

  reset_output_dir(out)

  # Copy the single shared image into /public/ so all pages can reference "/picture.png".
  copy_site_image(src_dir=script_dir, out_dir=out, filename=CONFIG.image_filename)

  # Core pages
  write_text(out / "index.html", homepage_html())
  write_text(out / "cost" / "index.html", cost_page_html())
  write_text(out / "how-to" / "index.html", howto_page_html())
  write_text(out / "contact" / "index.html", contact_page_html())

  # City pages
  for city, state, col in CITIES:
      write_text(out / city_state_slug(city, state) / "index.html", city_page_html(city, state, col))

  # robots + sitemap + wrangler
  urls = ["/", "/cost/", "/how-to/"] + [f"/{city_state_slug(c, s)}/" for c, s, _ in CITIES]
  write_text(out / "robots.txt", robots_txt())
  write_text(out / "sitemap.xml", sitemap_xml(urls))
  write_text(script_dir / "wrangler.jsonc", wrangler_content())

  print(f"✅ Generated {len(urls)} pages into: {out.resolve()}")


if __name__ == "__main__":
    main()
