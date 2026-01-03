#!/usr/bin/env python3
"""
Static site generator (no JS) for a single-service, multi-city site.

Cloudflare Pages:
- Build command: (empty)
- Output directory: public

URL structure:
- /<city>-<state>/   e.g. /los-angeles-ca/
- /cost/
- /how-to/

SEO rules enforced:
- Exactly one H1 per page
- <title> == H1
- Title <= 70 characters
- Main + City pages use the exact same H2 set (Ahrefs-driven)
- Cost and How-To use distinct H2 sets (no reused headings across them)
- Pure CSS, barebones, fast
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import html
import re
import shutil


# -----------------------
# CONFIG
# -----------------------
@dataclass(frozen=True)
class SiteConfig:
    service_name: str = "Wasp Nest/Wasp Hive Removal & Wasp Control Services"
    brand_name: str = "Peephole Installation Company"
    cta_text: str = "Get Free Estimate"
    cta_href: str = "mailto:hello@example.com?subject=Free%20Quote%20Request"
    output_dir: Path = Path("public")
    image_filename: str = "picture.png"  # sits next to generate.py
    cost_low: int = 150
    cost_high: int = 450


CONFIG = SiteConfig()

CITIES: list[tuple[str, str]] = [
  ("New York", "NY"),
  ("Los Angeles", "CA"),
  ("Chicago", "IL"),
  ("Dallas", "TX"),
  ("Fort Worth", "TX"),
  ("Philadelphia", "PA"),
  ("Houston", "TX"),
  ("Atlanta", "GA"),
  ("Washington", "DC"),
  ("Hagerstown", "MD"),
  ("Boston", "MA"),
  ("Manchester", "NH"),
  ("San Francisco", "CA"),
  ("Oakland", "CA"),
  ("San Jose", "CA"),
  ("Tampa", "FL"),
  ("St. Petersburg", "FL"),
  ("Sarasota", "FL"),
  ("Phoenix", "AZ"),
  ("Prescott", "AZ"),
  ("Seattle", "WA"),
  ("Tacoma", "WA"),
  ("Detroit", "MI"),
  ("Orlando", "FL"),
  ("Daytona Beach", "FL"),
  ("Melbourne", "FL"),
  ("Minneapolis", "MN"),
  ("St. Paul", "MN"),
  ("Denver", "CO"),
  ("Miami", "FL"),
  ("Fort Lauderdale", "FL"),
  ("Cleveland", "OH"),
  ("Akron", "OH"),
  ("Canton", "OH"),
  ("Sacramento", "CA"),
  ("Stockton", "CA"),
  ("Modesto", "CA"),
  ("Charlotte", "NC"),
  ("Raleigh", "NC"),
  ("Durham", "NC"),
  ("Fayetteville", "NC"),
  ("Portland", "OR"),
  ("St. Louis", "MO"),
  ("Indianapolis", "IN"),
  ("Nashville", "TN"),
  ("Pittsburgh", "PA"),
  ("Salt Lake City", "UT"),
  ("Baltimore", "MD"),
  ("San Diego", "CA"),
  ("San Antonio", "TX"),
  ("Hartford", "CT"),
  ("New Haven", "CT"),
  ("Kansas City", "MO"),
  ("Austin", "TX"),
  ("Columbus", "OH"),
  ("Greenville", "SC"),
  ("Spartanburg", "SC"),
  ("Asheville", "NC"),
  ("Anderson", "SC"),
  ("Cincinnati", "OH"),
  ("Milwaukee", "WI"),
  ("West Palm Beach", "FL"),
  ("Fort Pierce", "FL"),
  ("Las Vegas", "NV"),
  ("Jacksonville", "FL"),
  ("Harrisburg", "PA"),
  ("Lancaster", "PA"),
  ("Lebanon", "PA"),
  ("York", "PA"),
  ("Grand Rapids", "MI"),
  ("Kalamazoo", "MI"),
  ("Battle Creek", "MI"),
  ("Norfolk", "VA"),
  ("Portsmouth", "VA"),
  ("Newport News", "VA"),
  ("Birmingham", "AL"),
  ("Anniston", "AL"),
  ("Tuscaloosa", "AL"),
  ("Greensboro", "NC"),
  ("High Point", "NC"),
  ("Winston-Salem", "NC"),
  ("Oklahoma City", "OK"),
  ("Albuquerque", "NM"),
  ("Santa Fe", "NM"),
  ("Louisville", "KY"),
  ("New Orleans", "LA"),
  ("Memphis", "TN"),
  ("Providence", "RI"),
  ("New Bedford", "MA"),
  ("Fort Myers", "FL"),
  ("Naples", "FL"),
  ("Buffalo", "NY"),
  ("Fresno", "CA"),
  ("Visalia", "CA"),
  ("Richmond", "VA"),
  ("Petersburg", "VA"),
  ("Mobile", "AL"),
  ("Pensacola", "FL"),
  ("Fort Walton Beach", "FL"),
  ("Little Rock", "AR"),
  ("Pine Bluff", "AR"),
  ("Wilkes-Barre", "PA"),
  ("Scranton", "PA"),
  ("Hazleton", "PA"),
  ("Knoxville", "TN"),
  ("Tulsa", "OK"),
  ("Albany", "NY"),
  ("Schenectady", "NY"),
  ("Troy", "NY"),
  ("Lexington", "KY"),
  ("Dayton", "OH"),
  ("Tucson", "AZ"),
  ("Sierra Vista", "AZ"),
  ("Spokane", "WA"),
  ("Des Moines", "IA"),
  ("Ames", "IA"),
  ("Green Bay", "WI"),
  ("Appleton", "WI"),
  ("Honolulu", "HI"),
  ("Roanoke", "VA"),
  ("Lynchburg", "VA"),
  ("Wichita", "KS"),
  ("Hutchinson", "KS"),
  ("Flint", "MI"),
  ("Saginaw", "MI"),
  ("Bay City", "MI"),
  ("Omaha", "NE"),
  ("Springfield", "MO"),
  ("Huntsville", "AL"),
  ("Decatur", "AL"),
  ("Florence", "AL"),
  ("Columbia", "SC"),
  ("Madison", "WI"),
  ("Portland", "ME"),
  ("Auburn", "ME"),
  ("Rochester", "NY"),
  ("Harlingen", "TX"),
  ("Weslaco", "TX"),
  ("Brownsville", "TX"),
  ("McAllen", "TX"),
  ("Toledo", "OH"),
  ("Charleston", "WV"),
  ("Huntington", "WV"),
  ("Waco", "TX"),
  ("Temple", "TX"),
  ("Bryan", "TX"),
  ("Savannah", "GA"),
  ("Charleston", "SC"),
  ("Chattanooga", "TN"),
  ("Colorado Springs", "CO"),
  ("Pueblo", "CO"),
  ("Syracuse", "NY"),
  ("El Paso", "TX"),
  ("Las Cruces", "NM"),
  ("Paducah", "KY"),
  ("Cape Girardeau", "MO"),
  ("Harrisburg", "IL"),
  ("Shreveport", "LA"),
  ("Texarkana", "TX"),
  ("Champaign", "IL"),
  ("Urbana", "IL"),
  ("Springfield", "IL"),
  ("Decatur", "IL"),
  ("Burlington", "VT"),
  ("Plattsburgh", "NY"),
  ("Cedar Rapids", "IA"),
  ("Waterloo", "IA"),
  ("Iowa City", "IA"),
  ("Dubuque", "IA"),
  ("Baton Rouge", "LA"),
  ("Fort Smith", "AR"),
  ("Fayetteville", "AR"),
  ("Springdale", "AR"),
  ("Rogers", "AR"),
  ("Myrtle Beach", "SC"),
  ("Florence", "SC"),
  ("Boise", "ID"),
  ("Jackson", "MS"),
  ("South Bend", "IN"),
  ("Elkhart", "IN"),
  ("Johnson City", "TN"),
  ("Kingsport", "TN"),
  ("Bristol", "VA"),
  ("Greenville", "NC"),
  ("New Bern", "NC"),
  ("Washington", "NC"),
  ("Reno", "NV"),
  ("Davenport", "IA"),
  ("Rock Island", "IL"),
  ("Moline", "IL"),
  ("Tallahassee", "FL"),
  ("Thomasville", "GA"),
  ("Tyler", "TX"),
  ("Longview", "TX"),
  ("Lufkin", "TX"),
  ("Nacogdoches", "TX"),
  ("Lincoln", "NE"),
  ("Hastings", "NE"),
  ("Kearney", "NE"),
  ("Augusta", "GA"),
  ("Aiken", "SC"),
  ("Evansville", "IN"),
  ("Fort Wayne", "IN"),
  ("Sioux Falls", "SD"),
  ("Mitchell", "SD"),
  ("Johnstown", "PA"),
  ("Altoona", "PA"),
  ("State College", "PA"),
  ("Fargo", "ND"),
  ("Valley City", "ND"),
  ("Yakima", "WA"),
  ("Pasco", "WA"),
  ("Richland", "WA"),
  ("Kennewick", "WA"),
  ("Springfield", "MA"),
  ("Holyoke", "MA"),
  ("Traverse City", "MI"),
  ("Cadillac", "MI"),
  ("Lansing", "MI"),
  ("Youngstown", "OH"),
  ("Macon", "GA"),
  ("Eugene", "OR"),
  ("Montgomery", "AL"),
  ("Selma", "AL"),
  ("Peoria", "IL"),
  ("Bloomington", "IL"),
  ("Santa Barbara", "CA"),
  ("Santa Maria", "CA"),
  ("San Luis Obispo", "CA"),
  ("Lafayette", "LA"),
  ("Bakersfield", "CA"),
  ("Wilmington", "NC"),
  ("Columbus", "GA"),
  ("Monterey", "CA"),
  ("Salinas", "CA"),
  ("La Crosse", "WI"),
  ("Eau Claire", "WI"),
  ("Corpus Christi", "TX"),
  ("Salisbury", "MD"),
  ("Amarillo", "TX"),
  ("Wausau", "WI"),
  ("Rhinelander", "WI"),
  ("Columbus", "MS"),
  ("Tupelo", "MS"),
  ("West Point", "MS"),
  ("Starkville", "MS"),
  ("Columbia", "MO"),
  ("Jefferson City", "MO"),
  ("Chico", "CA"),
  ("Redding", "CA"),
  ("Rockford", "IL"),
  ("Duluth", "MN"),
  ("Superior", "WI"),
  ("Medford", "OR"),
  ("Klamath Falls", "OR"),
  ("Lubbock", "TX"),
  ("Topeka", "KS"),
  ("Monroe", "LA"),
  ("El Dorado", "AR"),
  ("Beaumont", "TX"),
  ("Port Arthur", "TX"),
  ("Odessa", "TX"),
  ("Midland", "TX"),
  ("Palm Springs", "CA"),
  ("Anchorage", "AK"),
  ("Minot", "ND"),
  ("Bismarck", "ND"),
  ("Dickinson", "ND"),
  ("Williston", "ND"),
  ("Panama City", "FL"),
  ("Sioux City", "IA"),
  ("Wichita Falls", "TX"),
  ("Lawton", "OK"),
  ("Joplin", "MO"),
  ("Pittsburg", "KS"),
  ("Albany", "GA"),
  ("Rochester", "MN"),
  ("Mason City", "IA"),
  ("Austin", "MN"),
  ("Erie", "PA"),
  ("Idaho Falls", "ID"),
  ("Pocatello", "ID"),
  ("Jackson", "WY"),
  ("Bangor", "ME"),
  ("Gainesville", "FL"),
  ("Biloxi", "MS"),
  ("Gulfport", "MS"),
  ("Terre Haute", "IN"),
  ("Sherman", "TX"),
  ("Ada", "OK"),
  ("Missoula", "MT"),
  ("Binghamton", "NY"),
  ("Wheeling", "WV"),
  ("Steubenville", "OH"),
  ("Yuma", "AZ"),
  ("El Centro", "CA"),
  ("Billings", "MT"),
  ("Abilene", "TX"),
  ("Sweetwater", "TX"),
  ("Bluefield", "WV"),
  ("Beckley", "WV"),
  ("Oak Hill", "WV"),
  ("Hattiesburg", "MS"),
  ("Laurel", "MS"),
  ("Rapid City", "SD"),
  ("Dothan", "AL"),
  ("Utica", "NY"),
  ("Clarksburg", "WV"),
  ("Weston", "WV"),
  ("Harrisonburg", "VA"),
  ("Jackson", "TN"),
  ("Quincy", "IL"),
  ("Hannibal", "MO"),
  ("Keokuk", "IA"),
  ("Charlottesville", "VA"),
  ("Lake Charles", "LA"),
  ("Elmira", "NY"),
  ("Corning", "NY"),
  ("Watertown", "NY"),
  ("Bowling Green", "KY"),
  ("Marquette", "MI"),
  ("Jonesboro", "AR"),
  ("Alexandria", "LA"),
  ("Laredo", "TX"),
  ("Butte", "MT"),
  ("Bozeman", "MT"),
  ("Bend", "OR"),
  ("Grand Junction", "CO"),
  ("Montrose", "CO"),
  ("Twin Falls", "ID"),
  ("Lafayette", "IN"),
  ("Lima", "OH"),
  ("Great Falls", "MT"),
  ("Meridian", "MS"),
  ("Cheyenne", "WY"),
  ("Scottsbluff", "NE"),
  ("Parkersburg", "WV"),
  ("Greenwood", "MS"),
  ("Greenville", "MS"),
  ("Eureka", "CA"),
  ("San Angelo", "TX"),
  ("Casper", "WY"),
  ("Riverton", "WY"),
  ("Mankato", "MN"),
  ("Ottumwa", "IA"),
  ("Kirksville", "MO"),
  ("St. Joseph", "MO"),
  ("Fairbanks", "AK"),
  ("Zanesville", "OH"),
  ("Victoria", "TX"),
  ("Helena", "MT"),
  ("Presque Isle", "ME"),
  ("Juneau", "AK"),
  ("Alpena", "MI"),
  ("North Platte", "NE"),
  ("Glendive", "MT"),
]


BRAND_NAME = "Woodpecker Damage Repair Company"

H1_TITLE = "Woodpecker Damage Repair/Wood Siding & EIFS Services"

COST_TITLE = "Woodpecker Damage Repair Cost"

HOWTO_TITLE = "How to Repair Woodpecker Damage"


# =========================
# MAIN PAGE (H2_SHARED)
# =========================

H2_SHARED = [
    "What Is Woodpecker Damage to Houses?",
    "Why Woodpeckers Peck on Houses",
    "Common Types of Woodpecker Damage",
    "Woodpecker Holes in Wood and Cedar Siding",
    "Woodpecker Damage to EIFS and Stucco",
    "Professional Woodpecker Damage Repair vs DIY",
    "When to Hire a Woodpecker Damage Repair Service",
]

P_SHARED = [
    "Woodpecker damage occurs when woodpeckers peck, drill, or create holes in the exterior of a house. This damage commonly affects wood siding, cedar siding, EIFS, and stucco surfaces. Over time, repeated pecking can expose the structure to moisture intrusion and further deterioration.",

    "Woodpeckers peck on houses for several reasons, including searching for insects, creating nesting cavities, or establishing territory. Soft siding materials and hollow-sounding surfaces often attract repeated pecking behavior.",

    "Common types of woodpecker damage include small round holes, larger nesting cavities, clustered peck marks, and surface chipping. Left unaddressed, these openings allow water, pests, and air infiltration.",

    "Woodpecker holes in wood and cedar siding are especially common because these materials are softer and more attractive to birds. Repairing cedar siding requires proper filling, sealing, and color-matching to restore both appearance and protection.",

    "EIFS and stucco are also frequent targets for woodpeckers. Damage to these systems often involves punctures or cavities that require specialized EIFS patching and sealing techniques to prevent moisture damage.",

    "DIY woodpecker hole repair may seem straightforward, but improper filling or sealing can trap moisture or fail to stop repeat damage. Professional repair focuses on restoring the surface correctly while addressing underlying vulnerabilities.",

    "Hiring a professional is recommended when damage affects siding integrity, involves EIFS or stucco systems, or when repeated woodpecker activity continues despite temporary fixes."
]


# =========================
# HOW-TO PAGE (H2_HOWTO)
# =========================

H2_HOWTO = [
    "Can You Repair Woodpecker Damage Yourself?",
    "How to Fix Woodpecker Holes in a House",
    "How to Repair Woodpecker Holes in Wood Siding",
    "How to Repair Woodpecker Damage in Cedar Siding",
    "How to Repair Woodpecker Damage in EIFS or Stucco",
    "Common Mistakes When Repairing Woodpecker Holes",
    "When DIY Woodpecker Damage Repair Is Not Recommended",
]

P_HOWTO = [
    "Minor woodpecker damage can sometimes be repaired by homeowners, but success depends on the siding type and extent of the damage. Improper repairs may fail to stop repeat pecking or allow moisture intrusion. For widespread or recurring damage, professional {woodpecker damage repair services} are often the safer option.",

    "Fixing woodpecker holes in a house typically involves cleaning the damaged area, filling holes with appropriate exterior-grade filler, sanding the surface smooth, sealing the repair, and repainting or finishing to match the surrounding siding.",

    "Repairing woodpecker holes in wood siding requires using fillers designed for exterior wood, followed by proper sealing and paint. Skipping these steps can lead to rot or visible patching.",

    "Cedar siding repairs must be handled carefully to preserve the wood grain and appearance. Improper filling or painting can make repairs stand out and reduce siding durability.",

    "EIFS and stucco repairs involve specialized patch materials and sealing techniques. Incorrect repairs can compromise the moisture barrier and lead to costly structural issues.",

    "Common DIY mistakes include using interior fillers, failing to seal repairs properly, mismatching paint, and ignoring the cause of the woodpecker activity. These errors often result in repeat damage.",

    "DIY repair is not recommended when damage is extensive, affects EIFS or stucco systems, or when woodpeckers continue pecking after repairs. In these cases, contacting a provider that offers {woodpecker damage repair services} is the safest next step."
]


# =========================
# COST PAGE (H2_COST)
# =========================

H2_COST = [
    "How Much Does Woodpecker Damage Repair Cost?",
    "What Affects the Cost of Woodpecker Damage Repair?",
    "Cost to Repair Woodpecker Holes in Siding",
    "Woodpecker Damage Repair Cost for EIFS and Stucco",
    "Does Insurance Cover Woodpecker Damage?",
    "When Professional Woodpecker Damage Repair Is Worth the Cost",
]

P_COST = [
    "Woodpecker damage repair typically costs between $200 and $1,500, depending on the number of holes, siding type, and extent of damage. Many homeowners compare DIY repairs against professional {woodpecker damage repair services} before deciding.",

    "Repair costs are influenced by siding material, size and quantity of holes, accessibility, height of the repair area, and whether moisture damage is present behind the siding.",

    "Repairing woodpecker holes in wood or cedar siding generally costs less than repairing EIFS or stucco, which require specialized materials and techniques.",

    "EIFS and stucco repairs are often more expensive due to moisture barrier considerations and the need for precise patching to prevent future damage.",

    "Insurance coverage for woodpecker damage varies by policy. Some homeowners insurance plans may cover damage if it is sudden and accidental, while others consider it maintenance-related. Policy review is recommended.",

    "Professional repair is worth the cost when damage affects structural integrity, involves EIFS systems, or when repeat woodpecker activity continues. In these cases, professional {woodpecker damage repair services} provide long-term protection and peace of mind."
]


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


def city_h1(service: str, city: str, state: str) -> str:
    return clamp_title(f"{service} in {city}, {state}", 70)


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

/* IMPORTANT: nav links apply grey text; ensure CTA stays white in the toolbar */
.nav a.btn{
  color:#fff;
  background:var(--cta);
  border-color:rgba(0,0,0,0.04);
}
.nav a.btn:hover{background:var(--cta2)}
.nav a.btn:focus{outline:2px solid var(--cta2); outline-offset:2px}

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
  text-align:left;
}
.hero h1{
  margin:0;
  font-size:30px;
  letter-spacing:-0.03em;
  line-height:1.18;
}
.sub{margin:0; color:var(--muted); max-width:78ch; font-size:14px}

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
.img{
  margin-top:14px;
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--line);
  background:var(--soft);
  box-shadow:var(--shadow2);
}
.img img{display:block; width:100%; height:auto}

h2{
  margin:18px 0 8px;
  font-size:16px;
  letter-spacing:-0.01em;
}
p{margin:0 0 10px}
.muted{color:var(--muted); font-size:13px}
hr{border:0; border-top:1px solid var(--line); margin:18px 0}

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
  padding:12px 12px;
  font-weight:800;
  font-size:14px;
  box-shadow:0 10px 24px rgba(17,24,39,0.05);
}
.city-grid a:hover{
  transform:translateY(-1px);
  box-shadow:0 14px 28px rgba(17,24,39,0.08);
}

.callout{
  margin:16px 0 12px;
  padding:14px 14px;
  border-radius:14px;
  border:1px solid rgba(22,163,74,0.22);
  background:linear-gradient(180deg, rgba(22,163,74,0.08), rgba(22,163,74,0.03));
}
.callout-title{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:900;
  letter-spacing:-0.01em;
  margin:0 0 6px;
}
.badge{
  display:inline-block;
  padding:3px 10px;
  border-radius:999px;
  background:rgba(22,163,74,0.14);
  border:1px solid rgba(22,163,74,0.22);
  color:var(--ink);
  font-size:12px;
  font-weight:900;
}
.callout p{margin:0; color:var(--muted); font-size:13px}

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
  text-align:left;
}
.footer-inner h2{margin:0; font-size:18px}
.footer-links{display:flex; gap:12px; flex-wrap:wrap}
.footer-links a{color:var(--muted); text-decoration:none; font-size:13px; padding:6px 0}
.small{color:var(--muted); font-size:12px; margin-top:8px}
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


def base_html(*, title: str, canonical_path: str, description: str, current_nav: str, body: str) -> str:
    # title == h1 is enforced by callers; keep this thin.
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{esc(canonical_path)}" />
  <style>
{CSS}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="/">{esc(BRAND_NAME)}</a>
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
  </div>
</header>
""".rstrip()


def footer_block() -> str:
    return f"""
<footer>
  <div class="footer-inner">
    <h2>Next steps</h2>
    <p class="sub">Ready to move forward? Request a free quote.</p>
    <div>
      <a class="btn" href="{esc(CONFIG.cta_href)}">{esc(CONFIG.cta_text)}</a>
    </div>
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/cost/">Cost</a>
      <a href="/how-to/">How-To</a>
    </div>
    <div class="small">© {esc(BRAND_NAME)}. All rights reserved.</div>
  </div>
</footer>
""".rstrip()


def page_shell(*, h1: str, sub: str, inner_html: str) -> str:
    # Single image used everywhere. Since we copy picture.png into /public/,
    # it can be referenced as "/picture.png" from any route.
    img_src = f"/{CONFIG.image_filename}"
    return (
        header_block(h1=h1, sub=sub)
        + f"""
<main>
  <section class="card">
    <div class="img">
      <img src="{esc(img_src)}" alt="Service image" loading="lazy" />
    </div>
    {inner_html}
  </section>
</main>
"""
        + footer_block()
    ).rstrip()


# -----------------------
# CONTENT SECTIONS
# -----------------------
def shared_sections_html(*, local_line: str | None = None) -> str:
    local = f' <span class="muted">{esc(local_line)}</span>' if local_line else ""
    return f"""
<h2>{esc(H2_SHARED[0])}</h2>
<p>{esc(P_SHARED[0])}</</p>

<h2>{esc(H2_SHARED[1])}</h2>
<p>{esc(P_SHARED[1])}</</p>

<h2>{esc(H2_SHARED[2])}</h2>
<p>{esc(P_SHARED[2])}</</p>

<h2>{esc(H2_SHARED[3])}</h2>
<p>{esc(P_SHARED[3])}</</p>

<h2>{esc(H2_SHARED[4])}</h2>
<p>{esc(P_SHARED[4])}</</p>

<h2>{esc(H2_SHARED[5])}</h2>
<p>{esc(P_SHARED[5])}</</p>
""".rstrip()


def cost_sections_html() -> str:
    return f"""
<h2>{esc(H2_COST[0])}</h2>
<p>{esc(P_COST[0])}</p>

<h2>{esc(H2_COST[1])}</h2>
<p>{esc(P_COST[1])}</p>

<h2>{esc(H2_COST[2])}</h2>
<p>{esc(P_COST[2])}</p>

<h2>{esc(H2_COST[3])}</h2>
<p>{esc(P_COST[3])}</p>

<h2>{esc(H2_COST[4])}</h2>
<p>{esc(P_COST[4])}</p>

<h2>{esc(H2_COST[5])}</h2>
<p>{esc(P_COST[5])}</p>

<hr />

<p class="muted">
  Typical installed range (single nest, many homes): ${CONFIG.cost_low}–${CONFIG.cost_high}. Final pricing depends on access, nest location, and time on site.
</p>
""".rstrip()


def howto_sections_html() -> str:
    return f"""
<h2>{esc(H2_HOWTO[0])}</h2>
<p>{esc(P_HOWTO[0])}</p>

<h2>{esc(H2_HOWTO[1])}</h2>
<p>{esc(P_HOWTO[1])}</p>

<h2>{esc(H2_HOWTO[2])}</h2>
<p>{esc(P_HOWTO[2])}</p>

<h2>{esc(H2_HOWTO[3])}</h2>
<p>{esc(P_HOWTO[3])}</p>

<h2>{esc(H2_HOWTO[4])}</h2>
<p>{esc(P_HOWTO[4])}</p>

<h2>{esc(H2_HOWTO[5])}</h2>
<p>{esc(P_HOWTO[5])}</p>
""".rstrip()


def city_cost_callout_html(city: str, state: str) -> str:
    # Subtle, high-impact conversion element for city pages.
    return f"""
<div class="callout" role="note" aria-label="Typical cost range">
  <div class="callout-title">
    <span class="badge">Typical range</span>
    <span>${CONFIG.cost_low}–${CONFIG.cost_high} for one nest</span>
  </div>
  <p>
    In {esc(city)}, {esc(state)}, most pricing comes down to access and where the nest is located.
    If you want a fast, no-pressure estimate, use the “{esc(CONFIG.cta_text)}” button above.
  </p>
</div>
""".rstrip()


# -----------------------
# PAGE FACTORY
# -----------------------
def make_page(*, h1: str, canonical: str, description: str, nav_key: str, sub: str, inner: str) -> str:
    h1 = clamp_title(h1, 70)
    title = h1  # enforce title == h1
    return base_html(
        title=title,
        canonical_path=canonical,
        description=clamp_title(description, 155),
        current_nav=nav_key,
        body=page_shell(h1=h1, sub=sub, inner_html=inner),
    )


def homepage_html() -> str:
    h1 = H1_TITLE
    city_links = "\n".join(
        f'<li><a href="{esc("/" + city_state_slug(city, state) + "/")}">{esc(city)}, {esc(state)}</a></li>'
        for city, state in CITIES
    )
    inner = (
        shared_sections_html()
        + """
<hr />
<h2>Choose your city</h2>
<p class="muted">Select a city page for the same guide with a light local line.</p>
<ul class="city-grid">
"""
        + city_links
        + """
</ul>
<hr />
<p class="muted">
  Also available: <a href="/cost/">Wasp Nest Removal Cost</a> and <a href="/how-to/">How to Get Rid of Wasp Nest</a>.
</p>
"""
    )

    return make_page(
        h1=h1,
        canonical="/",
        description="Straight answers on wasp nest removal and wasp control.",
        nav_key="home",
        sub="How removal works, what prevents repeat activity, and when to call help.",
        inner=inner,
    )


def city_page_html(city: str, state: str) -> str:
    inner = (
        shared_sections_html(local_line=f"Serving {city}, {state}.")
        + city_cost_callout_html(city, state)
        + f"""
<hr />
<h2>Wasp Nest Removal Cost</h2>
<p class="muted">
  Typical installed range for one nest often falls around ${CONFIG.cost_low}–${CONFIG.cost_high}. Access and nest location drive most pricing.
  See the <a href="/cost/">cost page</a> for details.
</p>
"""
    )

    return make_page(
        h1=city_h1(H1_TITLE, city, state),
        canonical=f"/{city_state_slug(city, state)}/",
        description=f"Wasp nest removal and wasp control guide with local context for {city}, {state}.",
        nav_key="home",
        sub="Same core guide, plus a quick local note and a typical cost range.",
        inner=inner,
    )


def cost_page_html() -> str:
    return make_page(
        h1=COST_TITLE,
        canonical="/cost/",
        description="Typical wasp nest removal cost ranges and what changes pricing.",
        nav_key="cost",
        sub="Simple ranges and the factors that usually move the price.",
        inner=cost_sections_html(),
    )


def howto_page_html() -> str:
    return make_page(
        h1=HOWTO_TITLE,
        canonical="/how-to/",
        description="Clear steps for dealing with a wasp nest without making it worse.",
        nav_key="howto",
        sub="A practical guide that prioritizes safety and reduces repeat activity.",
        inner=howto_sections_html(),
    )


# -----------------------
# ROBOTS + SITEMAP
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

    # City pages
    for city, state in CITIES:
        write_text(out / city_state_slug(city, state) / "index.html", city_page_html(city, state))

    # robots + sitemap
    urls = ["/", "/cost/", "/how-to/"] + [f"/{city_state_slug(c, s)}/" for c, s in CITIES]
    write_text(out / "robots.txt", robots_txt())
    write_text(out / "sitemap.xml", sitemap_xml(urls))

    print(f"✅ Generated {len(urls)} pages into: {out.resolve()}")


if __name__ == "__main__":
    main()
