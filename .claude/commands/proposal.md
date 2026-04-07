# Proposal Generator

*Generates a complete client proposal by running a brand audit, lighthouse audit, and prospect research, then assembling the results into a branded HTML document and PDF.*

---

## Trigger

User runs `/proposal` and provides either a prospect URL or a category + location.

## Pre-flight Checks

Before anything else, verify:

1. **Agency config exists.** Read `config/agency-config.json`. If it doesn't exist, stop and say: "Run `/setup` first to configure your agency profile."

2. **WeasyPrint is available.** Run `which weasyprint` via Bash. If not found, say: "WeasyPrint is required for PDF generation. Run `pip install -r requirements.txt` to install it."

3. **Lighthouse is available.** Run `which npx` via Bash. If not found, say: "Node.js and npx are required for the Lighthouse audit. Install Node.js first."

If all checks pass, proceed.

---

## Input Collection

Parse the arguments to determine the input mode:

- **URL mode** — argument contains `http` or a domain pattern (e.g., `example.com`). Proceed directly to Phase 1 with that URL.
- **Discovery mode** — argument is a category + location (e.g., `dentists in Portland`, `restaurants Austin TX`). Proceed to Phase 0 first.
- **No arguments** — ask: "What should I build a proposal for? Give me a URL or a category + location (e.g., 'dentists in Portland')."

Also parse optional flags:
- **`--tier`** (optional). Values: `website-redesign`, `monthly-retainer`, `one-time-audit`, `hybrid`. If not provided, use the default from `config/agency-config.json` field `pricing_template`.
- **`--brand`** (optional). Values: `prospect` or `seller`. Default: `seller`. Controls whether the proposal uses the prospect's brand colors or the agency's brand colors.

---

## Phase 0: Lead Discovery (discovery mode only)

This phase runs only when the user provided a category + location instead of a URL.

Tell the user: "Finding [category] prospects in [location]..."

Run WebSearch queries **in parallel**:

1. `best [category] in [location]`
2. `[category] near [location]`
3. `top rated [category] [location]`

For the top 5 results that are actual businesses (not directories or aggregator sites), WebFetch their homepages **in parallel**.

For each business, do a quick scan:
- Business name and URL
- Google rating and review count (from search snippets)
- 2-3 opportunity signals visible from the homepage (missing meta description, no SSL, no mobile optimization, weak CTAs, no schema markup, generic design, missing contact form)

Rank the leads by opportunity density (number and severity of gaps). The business with the most opportunity signals is the top prospect.

Present the results using **AskUserQuestion** with the top prospect as the recommended default. Format the question like this:

Title: "Found [N] prospects. Here's the top match."

Body:
```
**Recommended: [#1 Business Name]** ([url]) — [N] opportunity signals
[list the signals: no SSL, missing meta descriptions, etc.]

Other prospects:
2. [Business Name] ([url]) — [brief signals]
3. [Business Name] ([url]) — [brief signals]
...

Pick a number, or "all" for batch mode.
```

Default value: "1"

If the user picks a number: set that business's URL as `CLIENT_URL` and name as `CLIENT_NAME`, then proceed to Phase 1.

If the user says "all": run Phases 1-7 sequentially for each selected business, generating a separate proposal for each. Confirm before starting: "That's [N] proposals. Each takes about 4-5 minutes. Proceed?"

---

## Input Finalization (URL mode)

For URL mode only:

Store the URL as `CLIENT_URL`. Strip trailing slashes. Ensure it has a protocol (default to `https://`).

Extract the domain name from the URL for use as a default client name. Ask the user: "What's the business name? (default: [domain name])"

---

## Phase 1: Prospect Research (60-90 seconds)

Tell the user: "Researching [business name]..."

Run the following WebSearch queries **in parallel** (all in a single message):

1. `"[business name]" [extracted domain]`
2. `"[business name]" reviews OR testimonials`
3. `site:linkedin.com/company "[business name]"`

Also WebFetch the homepage at `CLIENT_URL`.

From the results, compile:
- Business name, industry, location
- Google Business Profile: found/not found, rating, review count
- Social media presence: platforms found
- Key competitors: 2-3 if found
- Opportunity signals: specific gaps (outdated site, missing GMB, weak social, no SSL, missing meta descriptions, no online booking, few reviews, no clear CTA)

Create the `output/` directory if it doesn't exist (`mkdir -p output` via Bash).

Write results to `output/prospect-research.json`:
```json
{
  "business_name": "...",
  "url": "...",
  "industry": "...",
  "location": "...",
  "date": "YYYY-MM-DD",
  "overview": { "description": "..." },
  "online_presence": {
    "google_business": { "found": true, "rating": 4.5, "review_count": 120 },
    "social_media": [{ "platform": "facebook", "url": "..." }],
    "directories": []
  },
  "competitors": [{ "name": "...", "url": "...", "notes": "..." }],
  "opportunity_signals": ["...", "..."]
}
```

Display a brief progress update: "Found: [business name], [industry], [location]. [N] opportunity signals identified."

---

## Phase 2: Brand Audit (2-3 minutes)

Tell the user: "Running brand audit on [domain]..."

From the homepage content already fetched in Phase 1, identify up to 4 additional key pages:
1. About / About Us page
2. Services / Products page
3. Contact page
4. One blog post (most recent if available)

**WebFetch all additional pages in parallel** (one call per page, all in a single message).

Analyze all fetched pages across 4 dimensions:

### Voice & Messaging
- Voice characteristics (3-5 adjectives)
- Hero headline (exact text from homepage)
- Value proposition
- Top 3 messaging themes
- Language orientation (customer-centric vs company-centric ratio)
- Tone consistency across pages

### Visual Identity
- Brand colors from CSS (hex codes)
- Fonts from Google Fonts URLs or CSS font-family
- Design aesthetic (one-line)

### SEO Snapshot
For each page: title tag (text + length), meta description (text + length or "missing"), H1 tag.
Homepage only: check sitemap.xml, robots.txt, HTTPS, schema markup types.

### Conversion Signals
- CTA inventory: button/link text, page, placement (above/below fold)
- Trust elements: testimonials, reviews, case studies, client logos, certifications
- Lead capture mechanisms: forms, chat, phone, scheduling, newsletter
- Above-fold CTA: present/missing, text

Rate each dimension: **Strong** / **Adequate** / **Weak**

Identify top 3 strengths and top 3 quick wins.

Write results to `output/brand-audit.json`:
```json
{
  "business_name": "...",
  "url": "...",
  "date": "YYYY-MM-DD",
  "pages_analyzed": [],
  "scores": {
    "voice_messaging": "Strong|Adequate|Weak",
    "visual_identity": "Strong|Adequate|Weak",
    "seo": "Strong|Adequate|Weak",
    "conversion": "Strong|Adequate|Weak"
  },
  "voice": {
    "characteristics": [],
    "headline": "...",
    "value_proposition": "...",
    "messaging_themes": [],
    "language_orientation": { "customer_centric": 60, "company_centric": 40 },
    "tone_consistency": "..."
  },
  "visual": {
    "colors": [{ "hex": "...", "name": "..." }],
    "fonts": { "heading": "...", "body": "..." },
    "aesthetic": "..."
  },
  "seo": {
    "pages": [{ "url": "...", "title": { "text": "...", "length": 0 }, "meta_description": { "text": "...", "length": 0 }, "h1": "..." }],
    "schema_types": [],
    "sitemap": true,
    "robots_txt": true,
    "https": true
  },
  "conversion": {
    "ctas": [{ "page": "...", "text": "...", "placement": "above-fold" }],
    "trust_elements": { "testimonials": 0, "case_studies": 0, "client_logos": 0 },
    "lead_capture": [],
    "above_fold_cta": { "present": true, "text": "..." }
  },
  "strengths": [],
  "quick_wins": []
}
```

Display progress: "Brand audit complete. [Score summary]."

---

## Phase 3: Lighthouse Audit (30-60 seconds)

Tell the user: "Running Lighthouse performance audit..."

Run via Bash:
```
npx lighthouse CLIENT_URL --output=json --output-path=stdout --chrome-flags="--headless=new --no-sandbox" --only-categories=performance,accessibility,best-practices,seo 2>/dev/null
```

Parse the JSON output. Extract:
- Category scores (multiply by 100): Performance, Accessibility, Best Practices, SEO
- Core Web Vitals: FCP, LCP, TBT, CLS, Speed Index
- Top 5 failing audits for categories below 90

Write to `output/lighthouse-audit.json`:
```json
{
  "url": "...",
  "date": "YYYY-MM-DD",
  "scores": {
    "performance": 72,
    "accessibility": 88,
    "best_practices": 95,
    "seo": 82
  },
  "core_web_vitals": {
    "fcp_seconds": 1.8,
    "lcp_seconds": 2.5,
    "tbt_ms": 150,
    "cls": 0.12,
    "speed_index_seconds": 3.2
  },
  "top_issues": [
    { "category": "...", "title": "...", "description": "...", "savings": "..." }
  ]
}
```

If Lighthouse fails: note "Lighthouse audit unavailable" and continue without it. The proposal will omit the Performance Audit section.

Display progress: "Lighthouse complete. Performance: [score], SEO: [score]."

---

## Phase 4: Synthesis & Recommendations

Read all three JSON files from `output/`.

Read the agency config from `config/agency-config.json`.

Read the selected pricing template from `config/pricing-templates/[tier].json`.

Generate prioritized recommendations by mapping the audit findings to agency services:
- Each quick win from the brand audit maps to a recommended action
- Each top Lighthouse issue maps to a recommended action
- Each opportunity signal from prospect research maps to a recommended action
- Tag each recommendation with the relevant agency service (from the services list in agency config)
- Prioritize by impact: items that affect conversion and revenue first, then SEO, then aesthetics

Generate an executive summary: 3-4 sentences synthesizing what was found, why it matters, and what you recommend. Reference specific scores and findings.

---

## Phase 5: Generate HTML Proposal

Read the template from `templates/proposal.html`.

Populate all template variables by replacing `{{ placeholder }}` tokens with actual content:

**Cover page variables:**
- `{{ agency_name }}` — from agency config
- `{{ agency_tagline }}` — from agency config (if present)
- `{{ client_name }}` — collected in input
- `{{ date }}` — today's date
- `{{ proposal_title }}` — "Digital Proposal"

**Brand variables (based on --brand flag):**
- If `seller`: use agency brand colors from config (`primary_color`, `secondary_color`)
- If `prospect`: use colors extracted from the brand audit

**Content sections:**
- `{{ executive_summary }}` — generated in Phase 4
- `{{ brand_audit_score_cards }}` — HTML score cards from brand audit scores
- `{{ brand_audit_voice_details }}` — HTML detail-grid rows
- `{{ brand_audit_visual_details }}` — HTML detail-grid rows with color swatches
- `{{ brand_audit_seo_table }}` — HTML table rows
- `{{ brand_audit_tech_checks }}` — HTML tech-check cards
- `{{ brand_audit_conversion }}` — HTML for CTAs, trust, lead capture
- `{{ lighthouse_score_cards }}` — HTML score cards with numeric scores
- `{{ lighthouse_vitals }}` — HTML vital cards
- `{{ lighthouse_issues }}` — HTML issue items
- `{{ recommendations_intro }}` — intro paragraph for recommendations
- `{{ recommendations }}` — HTML rec-items
- `{{ investment_intro }}` — intro paragraph for pricing
- `{{ pricing_tiers }}` — HTML tier cards from selected template
- `{{ next_steps_text }}` — closing paragraph with CTA
- `{{ agency_email }}`, `{{ agency_phone }}`, `{{ agency_website }}` — from config

**Generate the HTML string** by reading `templates/proposal.html` and replacing all `{{ }}` tokens with the generated HTML content.

Create a filename slug from the client name: lowercase, replace spaces with hyphens, remove special characters.

Write the completed HTML to `output/proposal-[slug].html`.

Display progress: "HTML proposal generated."

---

## Phase 6: Generate PDF

Run via Bash:
```
python3 scripts/generate_pdf.py output/proposal-[slug].html output/proposal-[slug].pdf
```

If the PDF generation fails, display the error and note that the HTML version is still available.

---

## Phase 7: Deliver

Also write `output/proposal-[slug].md` with a markdown version of the proposal content (executive summary, key findings, recommendations, pricing).

Open the PDF for the user:
```
open output/proposal-[slug].pdf
```

Display the final summary:

```
Proposal complete for [client name].

Files generated:
- output/proposal-[slug].html — open in browser for interactive view
- output/proposal-[slug].pdf — print-ready PDF
- output/proposal-[slug].md — markdown version

Data files:
- output/brand-audit.json
- output/lighthouse-audit.json
- output/prospect-research.json

Brand audit: [4 dimension scores]
Lighthouse: Performance [X], Accessibility [X], Best Practices [X], SEO [X]
Pricing tier: [template name] — [tier names and prices]
```

---

## Voice & Style Rules

Same as brand-audit:
- Direct, no preamble. Lead with findings, not methodology.
- Use concrete language: cite specific scores, name specific elements.
- No corporate filler.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT hedge.
- Progress updates should be brief: "Running Lighthouse..." not "I'm now going to run a Lighthouse performance audit on the website."

## Error Handling

- **Agency config missing:** "Run `/setup` first to configure your agency profile." Stop.
- **WeasyPrint not installed:** "Run `pip install -r requirements.txt` to install PDF dependencies." Stop.
- **Lighthouse fails:** Skip performance section. Note in output. Continue with brand audit and prospect research.
- **WebFetch fails on URL:** "I couldn't reach that URL. Check that the site is live and publicly accessible." Stop.
- **PDF generation fails:** Display error. Note that HTML version is available at the output path.
- **Pricing template not found:** List available templates in `config/pricing-templates/` and ask user to choose.

## What This Skill Does NOT Do

- Does not send the proposal to anyone
- Does not create accounts or authenticate with external services
- Does not spawn subagents or teams
- Does not modify the agency config or pricing templates
- Does not require any API keys beyond what Claude Code and the system provide
