# Master Outline & Study Guide
## Car Catalog — a source-cited vehicle dataset + offline static catalog (Vanilla JS, JSON, no build step)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One thing to internalize before anything else:** the *dataset* is the asset; the
> *catalog site* is the demonstration; the *verification system* is the gate; the
> *16-session workflow* is what made it scale. If you remember that sentence, you can
> reconstruct the whole project from it.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack at a Glance](#3-the-tech-stack-at-a-glance)
4. [End-to-End Architecture](#4-end-to-end-architecture)
5. [The Dataset — the Asset (Schema Deep Dive)](#5-the-dataset--the-asset-schema-deep-dive)
6. [Schema Versioning (v1.0 → v1.3)](#6-schema-versioning-v10--v13)
7. [The Source Policy](#7-the-source-policy)
8. [The Front-End Catalog (`app.js`)](#8-the-front-end-catalog-appjs)
9. [The Image Pipeline](#9-the-image-pipeline)
10. [The Verification System (`verify_brand.mjs`)](#10-the-verification-system-verify_brandmjs)
11. [Build & Deploy](#11-build--deploy)
12. [The 16-Session Engineering Workflow](#12-the-16-session-engineering-workflow)
13. [War Stories — What the Verification System Caught](#13-war-stories--what-the-verification-system-caught)
14. [Example Analyses](#14-example-analyses)
15. [Key Results & Numbers](#15-key-results--numbers)
16. [Limitations & Honest Accounting](#16-limitations--honest-accounting)
17. [Design Decisions & Trade-offs (the "Why")](#17-design-decisions--trade-offs-the-why)
18. [Interview Q&A](#18-interview-qa)
19. [How to Walk Through This Project Live](#19-how-to-walk-through-this-project-live)
20. [Glossary](#20-glossary)

---

## 1. The 30-Second Pitch

This project is a **structured, source-cited dataset of every current-model-year (2026)
vehicle sold new in the US** — **46 brands, 435 models, 1,492 trims**, roughly **40 spec
fields per row** — paired with a **vanilla-JavaScript single-page catalog** that renders
the dataset and works **fully offline** (you can open `index.html` by double-clicking it;
no server, no backend, no build step).

The interesting work is not the website — it's the **data layer and the discipline used to
build it**: schema-versioned JSON, a **manufacturer-only source policy enforced per field**,
and a **verification system** (Node.js scripts) that flags forbidden sources, schema
violations, and coverage gaps before anything ships. Every spec value traces back to a
manufacturer or government URL.

It was built across **16 chained Claude Code (AI-orchestrated) engineering sessions over
six days**, each with an explicit brief, named safety rules, mid-session checkpoints, and a
per-session summary report. The verification gates caught real failures — a silent regex
bug, and an external site serving anti-bot decoy images — before they corrupted the dataset.

**One-line version:** "I built a 1,492-row, fully source-cited vehicle dataset and an
offline, no-build catalog to browse it — and I built it through a disciplined,
16-session AI-orchestrated workflow with a verification system that gates every change."

**Live demo:** https://nadeaujonny.github.io/car-catalog/
**GitHub repo:** https://github.com/nadeaujonny/car-catalog

---

## 2. Why This Project Exists (Context)

**The original goal.** A personal reference catalog for car enthusiasts (originally an
audience of one) who want to *browse and learn brand lineups* — not a car-shopping tool.
The headline view: for each brand, every current model on one long-scroll page in
**ascending price order**, with full specs and real photos.

**What makes it a portfolio project.** It is deliberately *not* a framework showcase. It
demonstrates things that are harder and rarer than wiring up React:

- **Data engineering discipline** — designing a schema, evolving it safely, citing every
  field, and verifying the result programmatically.
- **Source provenance** — a documented, enforced policy about *where* data is allowed to
  come from, with the forbidden-source list encoded in a verifier.
- **Honest accounting** — the project documents exactly what it *couldn't* do (e.g., Tesla
  images) instead of papering over it.
- **AI-orchestrated engineering** — running a large build through 16 chained AI sessions
  with explicit safety rails, and being transparent about the trade-offs.

**Who it's framed for now.** A recruiter or engineer scanning the repo: the README leads
with the live demo and screenshots; the `docs/PROCESS.md` tells the engineering story; the
`SESSION_SUMMARY_*.md` files are the committed, inspectable record of how it was built.

---

## 3. The Tech Stack at a Glance

| Layer | Choice | Why it was chosen |
|---|---|---|
| **Front end** | Vanilla JavaScript (ES2020+), no framework | The data is the asset; the UI just makes it browsable. No React/Vue/bundler to version-pin or compile. |
| **Styling** | Hand-written CSS with custom properties; light + dark via `prefers-color-scheme` | No preprocessor, no Tailwind. ~2,000 lines, fully inspectable. |
| **Data format** | One JSON file per brand (`data/<brand>.json` ×46), fetched at runtime | Per-brand independence — no file can corrupt another. |
| **Build tools** | **None** — no bundler, transpiler, or task runner | Site opens from `file://` by double-clicking; same UX online and offline. |
| **Image scraping** | Node.js ESM scripts (`scripts/*.mjs`); Playwright as a JS-rendering fallback | Manufacturer image CDNs need careful per-host handling. |
| **Verification** | Node.js script (`verify_brand.mjs`), zero dependencies | Structural rules + forbidden-source detection encoded as code. |
| **Build step** | One small Python script (`build_catalog.py`) | Copies `data/` → `catalog/data/` and regenerates `manifest.json`. |
| **Analyses** | Python 3 + matplotlib only | Three standalone analysis scripts; the catalog itself has no Python runtime. |
| **Hosting** | GitHub Pages, deployed via GitHub Actions (`.github/workflows/deploy.yml`) | Push to `main` → Pages redeploys automatically. |
| **Build process** | 16 chained Claude Code (AI) sessions, version-controlled with Git | The orchestration workflow is itself part of the project's story. |

**The single most important stack fact:** there is **no toolchain**. The catalog is
`index.html` + `styles.css` + `app.js` + a folder of JSON. That portability is a deliberate
architectural decision, not a limitation (see §17).

---

## 4. End-to-End Architecture

The project has **four conceptual layers**. Understand the boundaries between them and you
understand the project.

```
  ┌─────────────────────────────────────────────────────────────┐
  │ LAYER 1 — THE DATASET (the asset)                            │
  │ data/<brand>.json  ×46                                        │
  │ Hand-built, schema-versioned (v1.3), every field source-cited │
  │ 46 brands · 435 models · 1,492 trims · ~40 fields/row         │
  └───────────────────────────┬─────────────────────────────────┘
                              │  build_catalog.py
                              │  (copies data/ → catalog/data/, builds manifest.json)
                              v
  ┌─────────────────────────────────────────────────────────────┐
  │ LAYER 2 — THE CATALOG SITE (the demonstration)               │
  │ catalog/index.html + styles.css + app.js + manifest.json      │
  │ Vanilla JS SPA. Loads manifest.json, lazy-loads brand JSONs,  │
  │ renders Home / Brand / Body-style / Compare views. No build.  │
  └───────────────────────────┬─────────────────────────────────┘
                              │  push to main
                              │  .github/workflows/deploy.yml
                              v
  ┌─────────────────────────────────────────────────────────────┐
  │ LAYER 3 — DEPLOY                                             │
  │ GitHub Actions uploads catalog/ as the Pages artifact        │
  │ Live at nadeaujonny.github.io/car-catalog/                   │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │ LAYER 4 — THE TOOLING (how the dataset was built & checked)  │
  │ scripts/verify_brand.mjs      — structural + source verifier  │
  │ scripts/scrape_image_urls.mjs — resolves image asset URLs     │
  │ scripts/download_images.mjs   — downloads images per-host     │
  │ scripts/brand-configs/<brand>.json — per-brand scraper hints  │
  │ analyses/*.py                 — example dataset analyses      │
  └─────────────────────────────────────────────────────────────┘
```

**The key architectural idea — the dataset is decoupled from everything else.** The catalog
front end is a *reader* of the dataset. The verifier is a *checker* of the dataset. The
analyses are *consumers* of the dataset. Nothing writes the dataset except the research
process and the gated image scripts. This is why a research pass on Hyundai cannot break
Toyota, and why the catalog could be rebuilt or replaced without touching a single data file.

**The "contract" between layers:**

- The **dataset** is the source of truth: `data/<brand>.json`.
- **`build_catalog.py`** mirrors `data/` into `catalog/data/` (kept byte-identical) and
  regenerates `catalog/manifest.json` (the brand index the site loads first).
- **`app.js`** reads `manifest.json`, then lazy-loads each `data/<slug>.json` on demand.
- **`verify_brand.mjs`** reads one `data/<brand>.json` and emits findings (blockers /
  warnings / FYIs).

---

## 5. The Dataset — the Asset (Schema Deep Dive)

This is the heart of the project. Interviewers will spend the most time here, so know it cold.

### 5.1 Top-level file shape

Each brand is **one self-contained JSON file** with no cross-file references:

```json
{
  "brand": "Honda",
  "brand_slug": "honda",
  "researched_at": "2026-05-11",
  "schema_version": "1.3",
  "models": [ /* one object per current-MY model */ ]
}
```

`researched_at` is an ISO date used for **drift detection** (compare against "now" to know
how stale a brand is). `schema_version` records which set of rules applied when the data
was written.

### 5.2 The three-level hierarchy: Brand → Model → Trim

- **Brand** — e.g., Honda. One JSON file.
- **Model** — a vehicle nameplate, e.g., Honda Civic. Note: *Civic Sedan* and *Civic
  Hatchback* are **separate models** because Honda sells them as separate body styles.
- **Trim** — a configurable variant of a model, e.g., Civic LX, Civic Sport. **One row of
  the dataset = one trim.** 1,492 trims = 1,492 rows.

### 5.3 The model object

Key model-level fields: `model`, `model_slug`, `model_year` (2026 for all current entries),
`body_style` (from a fixed 13-value taxonomy), `generation_context` (a one-line "which
generation, introduced when" note), `msrp_range` (`{low, high}`, computed from the trims),
`model_summary` (2–4 plain-prose sentences), `trims[]`, and four model-level review
sub-objects: `reliability`, `customer_satisfaction`, `professional_reviews`,
`owner_reviews`.

**Why reviews live at the model level, not the trim level:** reliability and satisfaction
scores aren't trim-specific — JD Power rates a *model*, not a *Civic Sport specifically*.
Putting them on the model avoids duplicating the same fact across every trim.

The four review sub-objects:

- **`reliability`** — JD Power VDS score (PP100, *lower is better*), JD Power VDS year,
  Consumer Reports predicted reliability (1–5), a `summary`, a `confidence` level, and a
  `sources` list.
- **`customer_satisfaction`** — JD Power APEAL. Most 2026 entries have a null APEAL score
  because the 2026 APEAL study hadn't been published yet (it typically publishes ~July).
- **`professional_reviews`** — a prose `summary` plus a 1–3 item `links` list of editorial
  reviews (each `{publication, url, date}`).
- **`owner_reviews`** — Edmunds / KBB star ratings + sample sizes (often null this early in
  a model year) and a `summary`.

Every review block carries a `confidence` field: `high` / `medium` / `low` / `unknown`.

### 5.4 The trim object and the base / step-up / delta pattern

**This is the single most important schema concept. Memorize it.**

A trim sheet duplicates 90%+ of its data from the trim below it. Rather than store full
specs on all 1,492 trims, the schema uses a **base-trim / step-up-trim** pattern:

- **The base trim** of each `trim_family` carries the **full spec** (`is_base_trim: true`).
- **Step-up trims** carry **only what changes** from base. Fields that don't differ are set
  to `null`, and the front end **inherits the value from the base trim** at render time.

**`trim_family`** is the grouping key. Trims in the same family share specs and can share
images. A multi-powertrain model splits into multiple families — the worked example:

```
Honda Accord — 6 trims, 2 powertrain families:
  LX        family=accord-ice     is_base_trim=true   → full ICE spec
  EX        family=accord-ice     is_base_trim=false  → deltas only
  EX-L      family=accord-ice     is_base_trim=false  → deltas only
  Sport     family=accord-hybrid  is_base_trim=true   → full hybrid spec
  Sport-L   family=accord-hybrid  is_base_trim=false  → deltas only
  Touring   family=accord-hybrid  is_base_trim=false  → deltas only
```

Each family has exactly one base trim carrying the full spec for that powertrain.

**`delta_from_base`** (step-up trims only) is a human-readable summary of what changed —
e.g., `{ "changes": ["19-inch alloy wheels", "leather seats"], "msrp_delta_usd": 5545,
"from_trim_slug": "lx" }`. The catalog renders it as the "Changes from base" column in the
trim table. The *source of truth* for what changed is the populated fields on the step-up
trim itself; `delta_from_base` is the readable summary on top.

### 5.5 The full-spec sub-objects (carried by base trims)

A base trim's full spec is organized into nested objects:

- **`powertrain`** — `type` (`ice` / `hybrid` / `phev` / `ev` / `fuel_cell`), engine
  displacement & config, aspiration, horsepower, torque, transmission, drivetrain
  (FWD/RWD/AWD/4WD).
- **`ev_specifics`** (EV/PHEV only) — battery capacity (total + usable kWh), electric
  range, total range, DC fast-charge peak kW, DC 10→80% minutes, AC charge kW, combined
  MPGe, plug type. *(Field names to know: `electric_range_mi`, `total_range_mi`,
  `dc_fast_charge_peak_kw`, `mpge_combined` — these are what `app.js` actually reads.)*
- **`fuel_economy`** — city / highway / combined MPG, fuel tank gallons, fuel type, EPA
  annual fuel cost. EVs mirror their MPGe values into the MPG fields so the schema stays
  homogeneous (see §6, v1.1).
- **`performance`** — 0–60 sec (with a `zero_to_60_source` recording where the number came
  from), top speed, towing capacity, payload.
- **`dimensions`** — length / width / height / wheelbase / ground clearance / curb weight,
  plus `cargo_volume_cuft` (trunk for sedans; `behind_2nd_row` / `behind_1st_row` for SUVs;
  `behind_3rd_row` added in v1.3 for three-row SUVs).
- **`capacity`** — seats, rows.
- **`wheels_tires`** — wheel size, tire spec.
- **`safety`** — NHTSA overall rating (1–5★), IIHS Top Safety Pick (`TSP` / `TSP+`), and a
  `standard_adas` object of 8 driver-assist booleans (AEB, lane keeping, adaptive cruise,
  blind-spot, etc.).
- **`features`** — infotainment & driver display sizes, CarPlay/Android Auto, sound system,
  sunroof, seat material, heated/ventilated seats, and a free-form `notable_other` list.
- **`warranty`** — basic / powertrain / corrosion / roadside / EV-battery / complimentary
  maintenance, each as a `"Nyr/Nk"` string.

### 5.6 The `sources` map — the project's signature feature

**Every trim has a `sources` map** recording the citation URL for each spec field. Keys are
field names (nested fields use dot notation); values are URLs:

```json
"sources": {
  "msrp_base": "https://www.hondainfocenter.com/2026/Civic-Sedan/",
  "powertrain": "https://www.motormatchup.com/catalog/Honda/Civic/2026/LX-CVT",
  "safety.nhtsa_overall_rating": "https://hondanews.com/.../releases/...",
  "safety.iihs_top_safety_pick": "https://www.iihs.org/ratings/vehicle/honda/civic-4-door-sedan/2026"
}
```

Schema v1.3 also adds an optional **`sources_confidence`** map (`high`/`medium`/`low` per
field) to flag fields where the *citation* was solid but the *value* was an editorial
estimate (e.g., a 0–60 time from MotorTrend rather than manufacturer-published).

### 5.7 Image entries

Each trim has an `images` array. The 4 required angles are `front_three_quarter`,
`rear_three_quarter`, `side_profile`, `interior_dashboard`. A typical entry has `angle`,
`url` (the direct asset URL), `local_path` (where the downloaded file lives in the repo),
`credit`, `is_shared_with_trim_family`, and `downloaded`. The **`needs_scraping: true`**
flag marks an entry whose direct asset URL wasn't findable at research time — a later
scrape pass resolves it (see §9). v1.3 added optional provenance fields: `source_tier`,
`source_domain`, `content_type`, `assignment_method`.

### 5.8 Edge cases worth knowing (interviewers probe these)

- **Singleton `trim_family`** — a family with exactly one trim. The rule (v1.1): it must be
  `is_base_trim: true`, `delta_from_base: null`, and carry the 4 required image angles in
  its own `images` array. The verifier enforces this; Session 12 cleaned up 56 Toyota
  violations via 49 minimal-diff family merges.
- **Ultra-luxury null MSRP** — Bentley, McLaren, Aston Martin, Rolls-Royce, Ferrari, and
  many Lamborghini trims don't publish prices. `msrp_base` stays `null`, the
  non-disclosure is documented in `trim.notes`, and the verifier downgrades it from a
  *blocker* to an *FYI*.
- **Multi-powertrain models** — split into multiple `trim_family` groups, one base trim
  each (the Accord example above).
- **EV MPGe mirroring** — EVs put their MPGe numbers into the `city/highway/combined_mpg`
  fields so the front end can render one field for every powertrain type.

---

## 6. Schema Versioning (v1.0 → v1.3)

The schema **evolved during the project** as edge cases surfaced. Each bump is documented
in `instructions/00_master_spec.md`. Being able to narrate this evolution shows you
understand that real schemas change and that change has to be managed.

| Version | What it added |
|---|---|
| **1.0** | The initial schema, written for the Honda pilot. |
| **1.1** | The singleton-trim rule (a sole-trim of a model carries the full spec, no delta); EV `customer_satisfaction` mirroring; per-field `sources_confidence`. |
| **1.2** | Body-style decision rules for tricky cases (LC 500 Convertible, Panamera Sport Turismo, Audi Sportback variants); the NHTSA/IIHS source-URL convention; ultra-luxury MSRP non-disclosure handling. |
| **1.3** | `behind_3rd_row` cargo field for three-row SUVs; the optional trim-level `sources_confidence` map; the `angle_url_patterns` brand-config field; optional image provenance fields. |

**The key decision:** when the schema changed, every brand was **re-verified against the
latest schema** at its next verification pass (rather than letting old brands sit on old
schemas forever). The version tag stays readable inside each brand JSON, so anyone can open
`data/honda.json`, see `"schema_version": "1.3"`, and know exactly which rules applied.

**Interview framing:** "I treated the schema as a versioned contract. When a new edge case
forced a change, I bumped the version, documented the changelog, and re-verified existing
brands against the new rules — so the dataset stays internally consistent rather than
fragmenting into per-brand dialects."

---

## 7. The Source Policy

This is the project's strongest "discipline" story. Know it well.

### 7.1 The default: manufacturer-only (Tier 1)

Every spec field must cite a **manufacturer URL** (`automobiles.honda.com`, `bmwusa.com`,
etc.). **Government sources** (`fueleconomy.gov` for EPA mileage/range, `nhtsa.gov` for
crash ratings, `iihs.org` for safety awards) and **JD Power** also count as Tier 1.

### 7.2 The forbidden-source list

Third-party aggregators, content farms, dealer sites, forums, and enthusiast wikis are
**forbidden**. The list includes `cars.com`, `motor1.com`, `carbuzz.com`, `autoblog.com`,
`autoevolution.com`, `topspeed.com`, `hotcars.com`, `iseecars.com`, Wikipedia, and a
dealer-domain hostname heuristic. The verifier (`verify_brand.mjs`) checks **every** source
URL against this list; any hit is a **blocker** — the brand fails verification.

### 7.3 Two scoped, documented relaxations

The policy isn't dogmatic — it has two *named, documented, verifier-aware* exceptions:

1. **Ultra-luxury MSRP** (added Session 9). Brands like Bentley, McLaren, Aston Martin,
   Rolls-Royce, Ferrari, and Lamborghini don't publish prices. For trims whose `notes`
   document the non-disclosure, MSRP may be cited from automotive press (Car and Driver,
   MotorTrend, Hagerty, Road & Track) at `medium` confidence. Cars.com, KBB, and dealer
   sites stay forbidden.
2. **Tier 2/3 image sources** (added Session 14). A small allowlist of press-kit
   aggregators is permitted for *images* when manufacturer sources produce nothing, with
   provenance fields recorded. **Tier 2 is currently dormant** — see the Session 15
   anti-bot story in §13.

**Why the policy matters:** Session 1's verification swept up content-farm citations
(cars.com, motor1.com) across multiple brands. Without an enforced policy, an AI-driven
research process will happily cite whatever ranks well in search. The manufacturer-only
rule plus the verifier is what kept the dataset's provenance clean.

---

## 8. The Front-End Catalog (`app.js`)

`app.js` is ~1,900 lines of plain ES2020+ JavaScript — no framework, no dependencies. It
renders the entire site. `styles.css` is ~2,000 lines of hand-written CSS.

### 8.1 How it boots

`<script src="app.js" defer>` runs `main()`, which: loads `manifest.json`, initializes the
top nav (brand & body-style dropdowns, search), wires up the modal, renders the footer,
runs `route()` for the current URL, and registers a `hashchange` listener.

### 8.2 Routing — hash-based, no router library

The app is a single page; "navigation" is **URL fragment** routing. `parseHash()` reads
`location.hash`, splits it into `key=value` params, and decides the view:

- `#brand=honda` → **Brand view**
- `#body=suv-midsize` → **Body-style view**
- `#compare=bmw:3-series:330i,...` → **Compare view**
- `#model=honda:civic` → Brand view with a deep-link scroll to that model
- empty → **Home view**

`route()` clears `<main>`, shows a soft loading spinner after 150ms, and calls the matching
`render*` function. Hash routing is what makes the site work from `file://` — there's no
server to do path-based routing.

### 8.3 The four views

- **Home** — hero with live counts (brands / models / trims), a brand-card grid (each card
  shows model count and price range), a body-style grid with hand-drawn line-art SVG icons,
  and a compare promo.
- **Brand view** — the headline view. One brand, every model on a long-scroll page. Each
  model renders as a section: title, generation context, MSRP range, a "Nth cheapest in the
  lineup" position label, hero image, quick-stat strip, collapsible spec blocks
  (`<details>` elements), the trim-delta table, an image gallery (opens a modal lightbox),
  the reviews block, and a footer with "Data sources" (opens a modal listing every cited
  URL) and "Open raw JSON". Has sort, filter (by body style, by powertrain), and
  group-by-body-style controls — all state stored in the URL hash.
- **Body-style view** — cross-brand: every midsize SUV (or sports car, etc.) from all
  brands, side by side, sortable.
- **Compare view** — pick 2–3 models or specific trims into slots; renders an aligned
  spec table where **differing rows are highlighted** and the "winner" cell (lowest price,
  highest horsepower, etc.) is marked.

### 8.4 Rendering details worth knowing

- **`el(tag, attrs, ...children)`** — a tiny ~25-line DOM helper used everywhere instead of
  a templating library or `innerHTML`. It's the project's "no framework" in microcosm.
- **`effectiveTrim(model, trim)`** — implements the base/step-up inheritance: for any null
  spec block on a step-up trim, it falls back to the base trim's value. This is the
  client-side half of the delta pattern.
- **`imageWithFallback()`** — tries `local_path`, then `url`, then a graceful
  **"image unavailable" placeholder**. Missing images never break layout and never show
  stale/wrong content.
- **Sort/filter/group state lives entirely in the URL hash** — so a filtered brand view is
  a shareable, bookmarkable link, and the browser back button works.
- **Search** builds an in-memory index (brands + models + trims) lazily on first keystroke,
  with keyboard navigation in the suggestions dropdown.
- **Sidenav scroll-spy** uses an `IntersectionObserver` to highlight the current model in
  the side navigation as you scroll.

---

## 9. The Image Pipeline

Images were the hardest part of the project. ~4,480 image slots; final coverage **72.58%**.

### 9.1 The two-script flow

1. **`scrape_image_urls.mjs`** — resolves image entries flagged `needs_scraping: true` into
   direct asset URLs. (When Phase 1 research couldn't find a direct `<img>` URL — often
   because a manufacturer page is JavaScript-rendered — it stored the *page* URL and set
   `needs_scraping: true`.) Playwright is used as a fallback to render JS-heavy pages.
2. **`download_images.mjs`** — downloads the resolved URLs into `catalog/images/` and sets
   `downloaded: true`.

### 9.2 The brand-config layer

Each brand has a `scripts/brand-configs/<slug>.json` — **not part of the dataset schema**,
a per-brand *hint file* for the scraper. It tells the scraper which manufacturer page to
fetch per model, alternate slug spellings, per-brand `angle_url_patterns` (regexes that map
a URL to an image angle), accepted CDN domains, and a path blacklist.

### 9.3 The "structural ceiling" concept

Coined in Session 7. The **structural ceiling** is the *upper bound on image coverage
achievable under the manufacturer-only policy* — i.e., what manufacturers actually publish
vs. what's gated behind configurators or login walls. Examples:

- **Tesla: 0%.** `tesla.com` and its configurator API return HTTP 403 to any non-browser
  client. No scraping engineering fixes this under the source policy.
- **Mercedes-Benz / Land Rover interiors** — routed through build-your-own configurators
  the script can't open.

The project reports **72.58% achieved coverage** and accounts for the remaining ~27% with
named structural ceilings per brand. Missing images render as honest placeholders — never
substituted or stale content. This is a core "honest accounting" talking point.

---

## 10. The Verification System (`verify_brand.mjs`)

**Verification is the gate. This is a top-three interview topic — know it deeply.**

`verify_brand.mjs` is a compact (~310-line) zero-dependency Node.js script. Run it as
`node scripts/verify_brand.mjs <brand_slug>` and it prints a JSON report. *(Note: the
repo's `PROCESS.md` narrative rounds this up to "~1,200 lines" — the committed script is
actually ~310 lines. If an interviewer reads both, mention the committed file is the
authority.)*

### 10.1 Three severity levels

- **Blockers** — schema violations or forbidden-source citations. **A brand with any
  blocker fails verification.**
- **Warnings** — pattern deviations that *may* be intentional (e.g., an ultra-luxury brand
  with no JD Power coverage). Informational.
- **FYIs** — expected observations, most commonly documented ultra-luxury MSRP
  non-disclosure.

### 10.2 What it checks

1. **Required keys** — every top-level, model, and trim key from the schema must be present.
2. **Forbidden sources** — every `sources` URL, every `professional_reviews.links[].url`,
   and every review-block source array is checked against the denylist and a dealer-domain
   heuristic. Hit → blocker.
3. **`msrp_range` consistency** — each model's `msrp_range.low/high` must equal the min/max
   of its trims' `msrp_base`. Drift → blocker.
4. **Base/step-up consistency** — a base trim must have `delta_from_base: null`; a step-up
   trim must have a non-null `delta_from_base`. `delta_from_base.from_trim_slug` must point
   at a real trim.
5. **Singleton trim_family rule** — a sole-trim family with 0 images is a blocker; with
   <4 images, a warning.
6. **Null MSRP handling** — a null `msrp_base` is a blocker *unless* `trim.notes` documents
   manufacturer non-disclosure (matched by regex), in which case it's downgraded to an FYI.
7. **Body-style ↔ dimensions sanity** — sedans should have a `trunk_cuft`; SUVs should have
   `behind_2nd_row`; mismatches are warnings.
8. **Cross-trim sanity** — MSRP outliers (a trim >2.1× the prior trim) are flagged as FYIs.
9. **EV/PHEV checks** — EV trims should carry `ev_specifics` and mirror MPGe into
   `fuel_economy`.

### 10.3 The verifier's own bug history (the meta-point)

The verifier is *itself code that can be wrong.* It was patched twice in Session 11:

- **`isDealerDomain` hostname-only fix.** The original regex matched the substring `of-`
  *anywhere* in a URL — so legitimate paths like Subaru's `benefits-of-ownership` and a
  Dodge press release about `horsepower-of-any-muscle-car` were flagged as dealer domains.
  The fix restricts matching to the parsed **hostname only** (`new URL(url).hostname`).
  This cleared ~27 false-positive blockers; a 19-test suite covers it.
- **Non-disclosure-aware MSRP downgrade.** The verifier was unconditionally blocking null
  `msrp_base`; the fix scans `trim.notes` for documented non-disclosure phrasing and
  downgrades to FYI.

**The lesson to state out loud:** "A verifier is an authority only if you periodically
audit its rules against the spec. Treating it as infallible meant real false-positives sat
flagged as blockers for weeks before the Session 11 audit caught them."

---

## 11. Build & Deploy

### 11.1 `build_catalog.py`

A small Python script (Phase 2 of the workflow). It does three things: copies every
`data/<brand>.json` into `catalog/data/` (keeping them byte-identical), regenerates
`catalog/manifest.json` (the brand index — slug, display name, `researched_at`, model
count, sorted alphabetically), and verifies that `index.html` / `styles.css` / `app.js`
still exist. It deliberately **does not touch the HTML/CSS/JS** — it's a data-and-manifest
refresh, not a site rebuild.

### 11.2 GitHub Pages deploy

`.github/workflows/deploy.yml` runs on every push to `main` (or manual
`workflow_dispatch`). It checks out the repo, configures Pages, uploads the **`catalog/`
directory** as the Pages artifact, and deploys. First-time setup requires choosing
"GitHub Actions" as the Pages source in repo settings.

Because there's no build step, the workflow is trivially short — there is nothing to
compile, just files to upload. This is the deploy-side payoff of the no-toolchain decision.

---

## 12. The 16-Session Engineering Workflow

The project was built across **16 chained Claude Code (AI-orchestrated) sessions over six
days (May 11–16, 2026)**. This workflow *is* part of the portfolio story — be ready to
discuss it honestly as a deliberate engineering choice.

### 12.1 What a session looked like

1. **Read the project state** — every session began by reading `PROJECT_STATE.md`, the most
   recent `SESSION_SUMMARY_N.md`, and `SESSION_NOTES.md` (~2 minutes). This prevented
   re-doing settled work.
2. **Execute phases against an explicit brief** — a multi-section prompt covering scope,
   phase structure, named safety rules, and explicit checkpoints.
3. **Save after every unit of work** — no batching. Every brand JSON write, every report,
   flushed to disk immediately, with a one-deep `.bak` backup before each mutation.
4. **Halt at checkpoints when reality diverged from the brief** — a checkpoint firing is
   the system *working*, not failing.
5. **Write artifacts** — every session ended with a `SESSION_SUMMARY_N.md` (concise),
   a `reports/session<N>_final.md` (detailed), and updates to `STATUS.md` /
   `PROJECT_STATE.md`. `SESSION_NOTES.md` logged halts append-only.

### 12.2 The named safety rules

Consolidated in `instructions/05_session_runbook.md`: instruction-file edits forbidden
unless explicitly authorized; `data/_partials/` (crash-safety partials) untouchable; brand
JSON mutations require a `.bak` backup first; `data/` and `catalog/data/` must stay in
sync; save after every operation; **if ambiguity arises outside a defined checkpoint,
write to `SESSION_NOTES.md` and stop — do not improvise.**

### 12.3 Parallel vs. single-threaded

The workflow parallelized **per-brand-independent** work (verification, research,
fix-passes) across subagents — 5–7 brands per agent — for roughly a 5× speedup. It kept
**shared-state** work (script edits, schema changes, instruction-file edits) strictly
single-threaded, because two agents editing the same file race.

### 12.4 The instruction files (the project's "process as code")

Seven instruction files in `instructions/` encode the repeatable process: `00_master_spec`
(the schema contract), `01_research_brand` (Phase 1), `02_build_catalog` (Phase 2),
`03_verify_catalog` (Phase 3), `04_scrape_images` (Phase 4), `05_session_runbook`
(multi-session meta-rules), `06_maintenance` (periodic upkeep).

### 12.5 The honest trade-offs

State these plainly — they make the story credible:

- **Verification is non-optional.** AI orchestration can produce a beautifully structured
  brand JSON in seconds; whether the cited URLs actually resolve is a question only
  verification answers.
- **Drift between sessions is a real risk.** A policy decided in Session 9 only stays
  consistent through Session 15 because the rationale was *written into an instruction
  file*, not left in chat memory.
- **Some work fits the pattern, some doesn't.** Per-brand work parallelizes; cross-file
  consistency work must be single-threaded.
- **Fresh-context cost.** ~2 minutes of orientation per session × 16 sessions = ~30
  minutes of pure overhead — worth it for coherence, but not free.

---

## 13. War Stories — What the Verification System Caught

These episodes are the best interview material in the whole project. Each one shows the
discipline producing a concrete save. Pick two or three and be able to tell them well.

### 13.1 The Honda pilot's 0-of-212 image download

The first image scrape downloaded **0 of 212** expected Honda images. Cause: Phase 1 had
stored consumer-site **page URLs** in `image.url`, expecting Phase 4 to extract the real
`<img src>` from them — but Phase 4 downloaded them as-is and got HTML, not images. **The
fix** created the page-vs-asset distinction and the `needs_scraping: true` workflow: store a
page URL with that flag, and a separate scrape pass resolves it to a direct asset URL.

### 13.2 The Wikimedia incident — search relevance ≠ accuracy

To lift Honda's image coverage, someone tested pulling from Wikimedia Commons. The test
pulled an image of a **1990s UK-market Civic Hatchback with a British license plate** and
labeled it as the 2026 Civic Hatchback. **The lesson, baked into the policy:**
search-result relevance is not image accuracy. Better to show a placeholder than a wrong
image. This is *why* the manufacturer-only policy is conservative.

### 13.3 Toyota's HTTP 403 and the Referer header

Toyota's first image run got 0% coverage — URLs extracted fine, but every download returned
HTTP 403. Toyota's CDN (`toyota.scene7.com`) only serves when the request `Referer` header
points to `toyota.com` (a browser sends this; a bare `fetch` doesn't). **The fix:** a
`PER_HOST_REFERER` map in `download_images.mjs`. Toyota jumped from 0% to 95%+ coverage. The
same shape of bug recurred for Hyundai and Subaru.

### 13.4 Session 9 — the silent regex separator bug

A per-brand image investigation found that `pickBestForAngle` had an **HTML-entity decode
bug**: Adobe AEM image URLs were embedded in JSON data layers with `&#34;` escapes the
extractor wasn't decoding. It had been **silently underperforming across multiple brands**.
Fixing one regex lifted Kia +45 percentage points of coverage, Ram +11, Ford +0.5. This
produced the project's "test the diagnosis" heuristic: *when a fix doesn't deliver the
expected magnitude, question the diagnosis rather than refine the fix.*

### 13.5 Session 15 — the anti-bot decoy images (the headline story)

Session 14 added NetCarShow as a permitted Tier 2 image source. Session 15 built a
heuristic that correctly identified 4 Ferrari hero images and downloaded them. **The
downloads looked perfect** — valid JFIF JPEG headers, realistic file sizes (113–185 KB),
correct content-type. But the session brief **required a visual spot-check** before
promoting Tier 2 project-wide. The spot-check failed: **all 4 files were anti-bot
pixel-noise decoys** — real JPEGs containing random-color mosaic, not Ferrari photography.
NetCarShow serves decoys to non-browser clients to defeat scraping.

Per the brief's safety rule, the session **reverted the 4 entries, deleted the 4 decoy
files, halted the project-wide pass, and demoted Tier 2 to dormant.** The checkpoint
discipline stopped bad data from propagating to other brands.

**The two lessons:** (1) HTTP-level success is a false signal — content must be
spot-checked, not just headers; (2) the checkpoint that "wasted" a session by halting it is
exactly the checkpoint working as designed.

### 13.6 Session 11 — the consolidation pass

By Session 10 the instruction files had drifted (multiple sessions adding clauses). Session
11 was a four-phase cleanup: consolidated the instruction files and bumped the schema to
v1.3; ran a forbidden-source fix-pass that dropped project blockers **271 → 56 (−79%)**;
applied pricing drift; re-verified. Session 12 then cleared the remaining 56 (all Toyota
singleton-no-image cases) via 49 minimal-diff family merges — taking **project-wide
blockers to 0 across all 46 brands**, a state that held through shipping.

---

## 14. Example Analyses

Three standalone Python scripts in `analyses/` (matplotlib only, ~150 lines each) read the
brand JSONs directly and demonstrate the dataset as an *analysis substrate*, not just a
browsing tool. Each follows the same pattern: load brand JSONs → walk model→trim → filter →
plot → print a markdown summary.

1. **Price–Performance Landscape** (`price_performance.py`) — MSRP vs horsepower (log-log)
   for ~900 trims, colored by powertrain. Findings: **PHEVs cluster in the luxury-
   performance tier** (median PHEV trim: 577 hp at $121,700) — PHEV tech is being used as a
   performance multiplier, not a mass-market efficiency play; the HP outlier is the
   **Bugatti Tourbillon at 1,800 hp / $4.1M**; best value by $/hp is the Rivian R2
   Performance ($88/hp).
2. **Brand Reliability Map** (`brand_reliability.py`) — JD Power 2026 VDS by brand (lower
   PP100 is better), vs the 204 industry average. Findings: **Lexus #1 (151), Buick #1
   mass-market (160); Volkswagen last (301)**, Volvo 296, Jeep 267. 16 of 46 brands have a
   published VDS score; the rest are null (EV-native or low-volume marques).
3. **EV Market Snapshot** (`ev_market.py`) — range vs price for 185 EV trims, bubble size =
   DC charging speed. Findings: the **Lucid Air Grand Touring leads range at 512 miles**;
   **Tesla Model 3/Y dominate the under-$50K range-per-dollar quadrant**; BMW iX3, Lucid
   Gravity, and Porsche Cayenne Electric peak at **400 kW** DC charging.

**A useful war story from building these:** the first EV analysis returned **0 rows**
because it filtered on guessed field names (`epa_range_mi`) instead of the dataset's actual
names (`electric_range_mi` / `total_range_mi`). Lesson: when an analysis claiming to filter
on field X returns 0 rows, first check that field X exists by that name.

---

## 15. Key Results & Numbers

Memorize these — interviewers love concrete figures.

| Metric | Value |
|---|---|
| Brands | **46** |
| Models | **435** |
| Trims (dataset rows) | **1,492** |
| Spec fields per row | **~40** |
| Image coverage | **3,253 / 4,482 = 72.58%** (manufacturer-sourced) |
| MSRP completion | **~98%** (the 2% gap is ultra-luxury non-disclosure) |
| Verification blockers | **0** across all 46 brands |
| Verification warnings / FYIs | ~312 warnings / ~30 FYIs (reviewed, expected) |
| Reliability data | JD Power 2026 VDS, current per model |
| Engineering sessions | **16** chained Claude Code sessions |
| Build timeline | 2026-05-11 → 2026-05-16 (6 days) |
| Schema version | evolved **v1.0 → v1.3** |
| `app.js` size | ~1,900 lines / ~77 KB, vanilla JS |
| `styles.css` size | ~2,000 lines / ~54 KB, hand-written |
| Build toolchain | **None** |
| Offline-capable | Yes — opens from `file://` |

---

## 16. Limitations & Honest Accounting

Volunteer these before you're asked — it signals engineering maturity. None are bugs; they
are scope or structural facts.

1. **Tesla is at 0% image coverage.** `tesla.com` and its configurator API return HTTP 403
   to any non-browser client. Tesla's *spec* data is complete (sourced from Tesla investor
   materials, EPA, IIHS); only images are missing, and the catalog renders Tesla with
   placeholders. A future fix would need Playwright-rendered scraping or a policy relaxation.
2. **~27% of images are missing overall** — Tesla, plus configurator-gated interior shots
   (Mercedes-Benz, Land Rover, Ferrari), unpublished 2026-MY photography, and sole-trim
   variants the manufacturer never shot separately. This is the **structural ceiling**:
   lifting it would require relaxing the source policy, which would compromise the citation
   discipline the rest of the project depends on.
3. **It's a snapshot, not a live feed.** `researched_at` is recorded per model; most brands
   were researched May 11–15, 2026. Trims change across model years; the dataset is not
   auto-refreshed. A quarterly freshness-check workflow is documented for upkeep.
4. **JD Power 2026 APEAL is mostly null** — the 2026 APEAL study hadn't published yet
   (typical July release). ~150–200 `customer_satisfaction` fields are queued to fill once
   it does. This is the only non-optional pending data work.
5. **No backend / no query layer.** All filtering and comparison run client-side over the
   JSON. The architecture is intentional, but there is no ad-hoc query interface beyond
   what the UI exposes (the analysis scripts fill that gap).
6. **Ultra-luxury MSRP gaps** — ~29 trims have null `msrp_base` because neither the
   manufacturer nor editorial sources publish a price (invite-only specials, bespoke
   commissions). Documented honestly rather than fabricated.
7. **The example analyses are illustrative, not exhaustive** — three of many possible
   slices of the data.

---

## 17. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. Here are the deliberate choices and their rationale.

**Why no front-end framework or build tools?**
The dataset is the asset; the UI just makes it browsable. A framework + bundler would add
compile steps, version pinning, and CI complexity that would dwarf the data work. The
no-toolchain choice also buys a real feature: the site works identically from `file://`,
from a local HTTP server, and from GitHub Pages. You can audit the entire front end by
reading three files.

**Why one JSON file per brand instead of one big dataset file?**
Independence. A research pass on Hyundai cannot corrupt Toyota. Parallel subagents can work
46 brands at once with no write collisions. A backup restore touches one file. The cost —
duplicating common reference data (taxonomies) in the verifier and front end — is the right
trade for a static dataset where per-brand independence pays back constantly.

**Why the base-trim / delta pattern instead of full specs per trim?**
Trim sheets duplicate 90%+ of their data. Storing full specs on every trim means verifying
the same fact 10 times for a 10-trim model and obscures the actual upgrade story. The delta
pattern surfaces "what does this trim actually add" directly, and the front end
reconstructs full specs by inheriting from base.

**Why manufacturer-only sourcing?**
An AI-driven research process will cite whatever ranks well in search — and Session 1's
verification proved it (content-farm citations across multiple brands). A documented,
verifier-enforced source policy is what keeps provenance trustworthy. The two relaxations
(ultra-luxury MSRP, Tier 2 images) are scoped and documented precisely so the policy
doesn't quietly erode.

**Why schema versioning with re-verification?**
Schema change mid-project is inevitable. The choice was between migrating old brands to new
versions or letting them carry stale schemas forever. Migrating (re-verifying every brand
against the latest schema) keeps the dataset internally consistent; the version tag stays
in each file as a readable historical artifact.

**Why the 16-session workflow with checkpoints and summaries?**
A single long agentic run produces no audit trail and no clean recovery point. Small,
scoped sessions with hard checkpoints between phases mean a failure is visible (in a
session summary) and recoverable (from a `.bak`). The Session 15 anti-bot halt followed a
rule *written ahead of time* — that's the difference between discipline and improvisation.

**Why verify with a script instead of manual review?**
1,492 trims × ~40 fields is too much to eyeball. Encoding the rules as code means every
brand is checked the same way, every time, and the check is itself reviewable and testable
(the `isDealerDomain` fix shipped with a 19-test suite).

**Why render placeholders for missing images instead of substituting?**
The Wikimedia incident. A wrong image (a 1990s UK Civic labeled as a 2026 Civic) is worse
than an honest blank. Fewer correct images beats more wrong ones.

---

## 18. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Walk me through this project end to end.**
"It's a source-cited dataset of every 2026 vehicle sold new in the US — 46 brands, 435
models, 1,492 trims, about 40 spec fields per trim — plus a vanilla-JavaScript catalog to
browse it. The dataset is one JSON file per brand, schema-versioned, with every field
carrying a citation URL. A small Python script copies the data into the catalog folder and
builds a manifest; the catalog is plain HTML, CSS, and JS with no build step, so it works
offline. A Node.js verifier checks every brand against the schema and a forbidden-source
list. I built the whole thing across 16 chained AI-orchestrated sessions, each with safety
rules and checkpoints, and it deploys to GitHub Pages on push."

**Q2. You said the dataset is the asset — what do you mean?**
"The website is just a reader. The real work is the data layer: designing a ~40-field
schema, evolving it through four versions as edge cases surfaced, citing every single field
to a manufacturer or government source, and verifying all of that programmatically. You
could throw away the front end and the dataset would still be the valuable artifact —
that's why I say the catalog is the demonstration, not the deliverable."

**Q3. What's the base-trim / delta pattern and why use it?**
"A trim sheet duplicates almost all of its data from the trim below it. So instead of
storing full specs on all 1,492 trims, the base trim of each trim-family carries the full
spec, and step-up trims store only what changes — everything else is null and inherited
from base at render time. It cuts redundancy, makes verification cheaper, and it surfaces
the actual upgrade story: what does this trim add over the one below it."

**Q4. How do you guarantee data quality across 1,492 rows?**
"Two things. First, a source policy: every field cites a manufacturer or government URL,
and a forbidden-source denylist blocks aggregators and content farms. Second, a verifier
script that checks every brand — required keys, forbidden sources, MSRP-range consistency,
the singleton-trim rule, base/step-up consistency — and classifies findings as blockers,
warnings, or FYIs. A brand with any blocker fails. The project shipped at zero blockers
across all 46 brands."

**Q5. Tell me about a bug the verification system caught.**
"The best one is Session 15. I'd added a press-kit aggregator as a Tier 2 image source. The
scraper found four Ferrari images and downloaded them — and they looked perfect: valid JPEG
headers, realistic file sizes, correct content-type. But the session brief required a
visual spot-check before going project-wide. The spot-check failed: all four were anti-bot
decoys — real JPEGs full of random pixel noise. The site serves those to non-browser
clients to defeat scraping. The checkpoint caught it, I reverted the four entries and
halted the rollout. The lesson: HTTP success is a false signal — you have to check the
content, not just the headers."

**Q6. Why no framework? Isn't vanilla JS a step backward?**
"For this project it's the right call. The data is the asset; the UI exists to make it
browsable. A framework plus a bundler would add a compile step, version pinning, and CI
complexity that would outweigh the actual UI work. And the no-build choice buys a real
feature — the site works identically by double-clicking the HTML file offline, from a local
server, or from GitHub Pages. If this were a large app with many engineers and complex
state, I'd reach for a framework. It isn't."

**Q7. What's the structural ceiling?**
"It's the honest upper bound on image coverage under the manufacturer-only policy — what
manufacturers actually publish, versus what's gated behind configurators or login walls.
Tesla is the clearest case: their site returns 403 to any non-browser client, so the
ceiling for Tesla is literally 0% — no scraping engineering changes that. The project
reports 72.58% achieved coverage and accounts for the remaining 27% with named ceilings per
brand, instead of pretending the gap is a to-do item."

**Q8. How does the schema handle EVs, which have different specs from gas cars?**
"There's an `ev_specifics` sub-object — range, battery capacity, DC charging speed, plug
type — that only EVs and PHEVs carry. And EVs mirror their MPGe numbers into the regular
MPG fields, so the front end can render one fuel-economy field for every powertrain type.
It's a slight semantic loosening in exchange for a homogeneous schema the UI can treat
uniformly."

**Q9. You built this with AI orchestration — isn't that just 'the AI did it'?**
"No — my role was design and orchestration. I wrote the session briefs, chose the phase
ordering, made the policy decisions — manufacturer-only sourcing, the scoped relaxations,
the schema changes — and reviewed every output. The AI is fast at breadth but it will cite
a content farm or produce a plausible-looking wrong value without blinking. The whole
verification system and the checkpoint discipline exist precisely because AI output has to
be verified rigorously. The project is transparent about this — the 16 session summaries
are committed to the repo."

**Q10. What were the hardest parts?**
"Images, by a wide margin. Manufacturer image CDNs each gate differently — Toyota needs a
Referer header, Hyundai needs a format query parameter, Tesla blocks everything. Each fix
was a small per-host patch, validated on one brand before applying to others. The other
hard part was keeping policy decisions consistent across 16 sessions — I solved that by
writing the rationale into instruction files instead of relying on memory."

**Q11. How do you know your sources are actually valid and not hallucinated?**
"The verifier checks every URL against a forbidden-source denylist and a dealer-domain
heuristic — that catches *category* violations. It doesn't fetch every URL to confirm it
resolves; that's a documented limitation. The verification phase does spot-check random
trims against live manufacturer pages, and the image scrape pass effectively validates a
subset of URLs by fetching them. A stronger version would add live URL resolution to the
verifier."

**Q12. If you extended this, what would you do next?**
"Three things. First, fill the JD Power APEAL fields once the 2026 study publishes — that's
the one piece of known-pending data. Second, lift Tier 2 images properly with a
Playwright-rendered fetch that can get past anti-bot decoys. Third, add live URL resolution
to the verifier so a dead or redirected citation is caught automatically. Beyond that, the
dataset is rich enough for a lot more analysis — drivetrain matrices, ADAS standardization
timelines, warranty positioning."

**Q13. Why is the verifier itself something you talk about as having had bugs?**
"Because a verifier is only an authority if you audit it. Mine had a regex that matched the
substring 'of-' anywhere in a URL, so legitimate paths like Subaru's 'benefits-of-
ownership' got flagged as dealer domains — about 27 false-positive blockers sat there for
weeks. Session 11 caught it and the fix shipped with a 19-test suite. The point I'd make in
an interview is that I treat verification code as code that can be wrong, not as gospel."

**Q14. How does the front end stay fast with 46 brands of data?**
"It lazy-loads. On boot it fetches only `manifest.json` — a small index of the 46 brands.
Each brand's full JSON is fetched on demand the first time you visit that brand, then
cached in memory. Views that need everything — the cross-brand body-style view, search —
load all brands once and reuse them. There's no framework re-render cost; rendering is
direct DOM construction."

**Q15. What does 'every field source-cited' actually look like in the data?**
"Each trim has a `sources` map — keys are field names, values are URLs. So
`sources['msrp_base']` is the manufacturer page the price came from;
`sources['safety.nhtsa_overall_rating']` is the NHTSA page. Nested fields use dot notation.
There's also an optional `sources_confidence` map that flags when a citation was solid but
the value itself was an editorial estimate. The catalog has a 'Data sources' button on
every model that lists every cited URL."

---

## 19. How to Walk Through This Project Live

If asked to screen-share, use this order:

1. **Open the live catalog.** Lead with the *outcome* — show the Home view's counts, click
   into a brand (BMW is a good one), scroll the long-scroll price-ascending page, expand a
   spec block, open the trim-delta table, hit "Data sources" to show the citations.
2. **Show the Compare view** — pick three trims, point out the highlighted differing rows.
3. **Show a raw `data/<brand>.json`** — this is the asset. Point at one trim: the nested
   spec objects, the `sources` map, `is_base_trim` / `delta_from_base`.
4. **Show `verify_brand.mjs`** — explain blockers vs. warnings vs. FYIs, and the
   forbidden-source check. Mention the `isDealerDomain` bug-fix as proof you audit your
   own tooling.
5. **Show `app.js`** — point at the `el()` helper (the "no framework" in one function),
   `parseHash()` routing, and `effectiveTrim()` (the base/step-up inheritance).
6. **Show a `SESSION_SUMMARY_*.md`** — explain the 16-session workflow and the checkpoint
   discipline.
7. **Close with a war story** — the Session 15 anti-bot decoy is the strongest. It shows
   the whole system working: a checkpoint catching a failure that looked like success.

**Pacing tip:** spend the most time on the dataset and the verifier. The front end is
clean but it's a reader; the data layer and the discipline are the differentiated work.

---

## 20. Glossary

- **Trim** — one configurable variant of a model (Civic LX). One trim = one dataset row.
- **Model** — a vehicle nameplate (Honda Civic). Body-style variants are separate models.
- **`trim_family`** — the grouping key for trims that share specs and images; each family
  has one base trim.
- **Base trim** — the trim carrying the full spec for its family (`is_base_trim: true`).
- **Step-up trim** — a non-base trim storing only `delta_from_base`; null fields inherit
  from base.
- **`delta_from_base`** — the human-readable summary of what a step-up trim changes.
- **Singleton trim_family** — a family with exactly one trim; must be a base trim with the
  4 required images.
- **Schema version** — the `"1.0"`–`"1.3"` tag recording which rule-set a brand's data
  follows.
- **Manufacturer-only policy** — the rule that every spec field cites a manufacturer or
  government URL.
- **Forbidden-source list** — the denylist of aggregators / content farms / dealer sites
  the verifier blocks.
- **Tier 1 / Tier 2 / Tier 3 sources** — Tier 1 = manufacturer/government (default); Tier
  2 = press-kit aggregators (images only, currently dormant); Tier 3 = manufacturer
  configurator endpoints.
- **Structural ceiling** — the honest upper bound on image coverage under the source
  policy (e.g., Tesla = 0%).
- **`needs_scraping`** — a flag on an image entry whose direct asset URL still needs to be
  resolved by a scrape pass.
- **Blocker / Warning / FYI** — the verifier's three severity levels; any blocker fails a
  brand.
- **VDS (Vehicle Dependability Study)** — JD Power's reliability metric, measured in PP100
  (problems per 100 vehicles); lower is better.
- **APEAL** — JD Power's customer-satisfaction study; for 2026 it publishes ~July.
- **PP100** — problems per 100 vehicles; the unit of the VDS score.
- **ADAS** — Advanced Driver-Assistance Systems (automatic emergency braking, lane keeping,
  etc.); stored as 8 booleans under `safety.standard_adas`.
- **MSRP** — Manufacturer's Suggested Retail Price; `msrp_base` per trim, `msrp_range` per
  model.
- **`manifest.json`** — the brand index the catalog loads first, before lazy-loading brand
  data.
- **Hash routing** — using the URL fragment (`#brand=honda`) for navigation; what lets the
  SPA work from `file://`.
- **Claude Code session** — one AI-orchestrated engineering session; the project ran 16,
  each with a brief, safety rules, checkpoints, and a summary report.
- **`.bak` discipline** — writing a one-deep backup before any file mutation so every step
  is recoverable.
- **Structural ceiling vs. coverage gap** — a *ceiling* is a documented hard limit; a
  *gap* is unfinished work. The project is careful to label which is which.

---

*This study guide documents the project as built. The authoritative references in the
repo are: the schema contract (`instructions/00_master_spec.md`), the engineering
narrative (`docs/PROCESS.md`), the schema tutorial (`docs/SCHEMA.md`), the front end
(`catalog/app.js`), and the verifier (`scripts/verify_brand.mjs`). When this guide and the
source disagree, the source wins.*
