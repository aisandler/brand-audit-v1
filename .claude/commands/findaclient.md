# Find a Client

*Guided workflow for prospecting and proposal generation. The user makes decisions, the system does everything else.*

---

## Trigger

User runs `/findaclient`. No arguments needed.

---

## Pre-flight

1. Read `config/agency-config.json`. If it doesn't exist, stop: "Run `/setup` first to configure your agency profile."
2. Extract `target_verticals`, `geographic_focus`, and `services` from the config.
3. Verify WeasyPrint: run `which weasyprint` via Bash. If not found: "Run `pip install -r requirements.txt` first."
4. Verify npx: run `which npx` via Bash. If not found: "Node.js is required for Lighthouse audits. Install Node.js first."

---

## Step 1: Choose a Category

Build a list of recommended search categories based on the agency config. For each target vertical, generate 2-3 specific business types that commonly need digital services. For example:

- If vertical is "restaurants": suggest "restaurants", "coffee shops", "catering companies"
- If vertical is "dental": suggest "dental practices", "orthodontists", "cosmetic dentists"
- If vertical is "law firms": suggest "personal injury lawyers", "family law attorneys", "estate planning firms"
- If vertical is "local-businesses": suggest "plumbers", "HVAC contractors", "auto repair shops", "salons", "fitness studios"

Use **AskUserQuestion** to present the options:

- Title: "What kind of business are you looking for?"
- Options: the generated category list, each formatted as "[category] in [geographic_focus]"
- Include a text input option for custom searches
- Default: the first recommended category

Example:

```
Title: "What kind of business are you looking for?"

Suggested based on your profile:

1. Plumbers in Austin, TX
2. HVAC contractors in Austin, TX
3. Auto repair shops in Austin, TX
4. Salons in Austin, TX
5. Fitness studios in Austin, TX
6. Restaurants in Austin, TX
7. Coffee shops in Austin, TX

Or type your own (e.g., "dentists in Portland")
```

Store the selected category and location.

---

## Step 2: Find Prospects

Tell the user: "Searching for [category] in [location]..."

Run WebSearch queries **in parallel**:

1. `best [category] in [location]`
2. `[category] near [location]`
3. `top rated [category] [location]`
4. `[category] [location] website`

For the top 5 results that are actual businesses (not directories like Yelp, Google Maps, Angi, Thumbtack, etc.), WebFetch their homepages **in parallel**.

For each business, do a quick scan of the homepage:
- Business name and URL
- Google rating and review count (from search snippets)
- Opportunity signals: count and list specific gaps
  - No SSL / not HTTPS
  - Missing or generic meta description
  - No H1 tag or duplicate H1
  - No schema markup
  - Missing contact form or lead capture
  - No clear CTA above the fold
  - Outdated or generic template design
  - No social media links
  - No Google Business Profile found in search results
  - Slow-loading indicators (large unoptimized images, no lazy loading)
  - Not mobile-responsive (no viewport meta tag)
  - No online booking or scheduling

Rank prospects by opportunity density (total number of gaps). The business with the most gaps is the strongest sales opportunity.

---

## Step 3: Pick a Prospect

Use **AskUserQuestion** to present the ranked leads:

- Title: "Found [N] prospects. Here's the best opportunity."
- Body: Present the top prospect with full detail, then the rest briefly.
- Default: "1"

Format:

```
**Top prospect: [Business Name]** ([url])
[N] opportunity signals: [list each signal]
Google: [rating] stars, [review count] reviews

Other prospects:
2. [Name] ([url]) — [N] signals: [brief list]
3. [Name] ([url]) — [N] signals: [brief list]
4. [Name] ([url]) — [N] signals: [brief list]
5. [Name] ([url]) — [N] signals: [brief list]

Pick a number to generate a full proposal.
```

Store the selected business URL as `CLIENT_URL` and name as `CLIENT_NAME`.

---

## Step 4: Deep Research

Tell the user: "Researching [CLIENT_NAME]..."

Run WebSearch queries **in parallel**:

1. `"[CLIENT_NAME]" [location]`
2. `"[CLIENT_NAME]" reviews OR testimonials`
3. `site:linkedin.com/company "[CLIENT_NAME]"`
4. `"[CLIENT_NAME]" competitors OR alternatives`

From the results, compile:
- Business overview: industry, location, years in business, size signals
- Online presence: Google Business Profile (rating, reviews), social media platforms found, directory listings
- Competitors: 2-3 local competitors with URLs
- Opportunity signals: expanded from the quick scan with additional detail

### Competitor Scan

For each competitor found (up to 3), **WebFetch their homepage in parallel**. For each competitor, do a quick check of:

- **HTTPS:** does the URL use https?
- **Meta description:** present or missing?
- **H1 tag:** present or missing?
- **Schema markup:** any structured data?
- **Mobile viewport:** has `<meta name="viewport">`?
- **Google Business Profile:** found in search results? Rating?
- **Social media links:** any social links on the page?
- **Online booking:** scheduling or booking link present?
- **Contact form:** form element on the page?
- **CTA above fold:** clear call-to-action in the first section?

Record the same checks for the prospect (from the homepage already fetched). This builds the data for the competitive comparison table in the proposal.

Create `output/` directory if it doesn't exist (`mkdir -p output` via Bash).

Write to `output/prospect-research.json`:
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
    "social_media": [{ "platform": "...", "url": "..." }],
    "directories": []
  },
  "competitors": [
    {
      "name": "...",
      "url": "...",
      "notes": "...",
      "signals": {
        "https": true,
        "meta_description": true,
        "h1_tag": true,
        "schema_markup": false,
        "mobile_viewport": true,
        "google_business": { "found": true, "rating": 4.2 },
        "social_media": true,
        "online_booking": false,
        "contact_form": true,
        "cta_above_fold": true
      }
    }
  ],
  "prospect_signals": {
    "https": false,
    "meta_description": false,
    "h1_tag": true,
    "schema_markup": false,
    "mobile_viewport": true,
    "google_business": { "found": false },
    "social_media": false,
    "online_booking": false,
    "contact_form": false,
    "cta_above_fold": false
  },
  "opportunity_signals": []
}
```

Display brief progress: "[CLIENT_NAME]: [industry] in [location]. [N] opportunity signals confirmed. [N] competitors scanned."

---

## Step 5: Brand Audit

Tell the user: "Running brand audit on [CLIENT_URL]..."

From the homepage content already fetched, identify up to 4 additional key pages:
1. About / About Us
2. Services / Products
3. Contact
4. One blog post (most recent)

**WebFetch all additional pages in parallel.**

Analyze all pages across 4 dimensions:

**Voice & Messaging:** voice characteristics (3-5 adjectives), hero headline, value proposition, messaging themes (top 3), language orientation (customer vs company ratio), tone consistency.

**Visual Identity:** brand colors from CSS (hex codes), fonts from Google Fonts or CSS, design aesthetic (one-line).

**SEO Snapshot:** per page: title tag (text + length), meta description (text + length or "missing"), H1. Homepage: sitemap.xml, robots.txt, HTTPS, schema markup.

**Conversion Signals:** CTA inventory (text, page, placement), trust elements (testimonials, reviews, case studies, logos, certifications), lead capture (forms, chat, phone, scheduling), above-fold CTA.

Rate each: **Strong** / **Adequate** / **Weak**. Identify top 3 strengths and top 3 quick wins.

Write to `output/brand-audit.json` (full schema as defined in brand-audit.md Phase 3.5).

Display progress: "Brand audit complete. Voice: [rating], Visual: [rating], SEO: [rating], Conversion: [rating]."

---

## Step 6: Lighthouse Audit

Tell the user: "Running Lighthouse on [CLIENT_URL]..."

Run via Bash:
```
npx lighthouse CLIENT_URL --output=json --output-path=stdout --chrome-flags="--headless=new --no-sandbox" --only-categories=performance,accessibility,best-practices,seo 2>/dev/null
```

Parse JSON output:
- Category scores (x100): Performance, Accessibility, Best Practices, SEO
- Core Web Vitals: FCP, LCP, TBT, CLS, Speed Index
- Top 5 failing audits for categories below 90

Write to `output/lighthouse-audit.json`.

If Lighthouse fails: note "Lighthouse unavailable" and continue. The proposal will skip the performance section.

Display progress: "Lighthouse complete. Performance: [score], SEO: [score]."

---

## Step 7: Choose Pricing

Read `config/agency-config.json` for the default pricing template.

Read the default template from `config/pricing-templates/[template].json`.

Use **AskUserQuestion** to confirm:

- Title: "Which pricing package fits this prospect?"
- Body: Show the default template name and tier summary. List alternatives.
- Default: the agency's default template name

Format:

```
Default: [Template Name]
[Tier 1] ($X) / [Tier 2] ($X) / [Tier 3] ($X)

Other options:
- website-redesign: Starter ($2,500) / Growth ($5,000) / Premium ($10,000)
- monthly-retainer: Essentials ($997/mo) / Growth ($2,500/mo) / Scale ($5,000/mo)
- one-time-audit: Deep Audit ($1,500)
- hybrid: Launch ($4K+$750/mo) / Accelerate ($7.5K+$1.5K/mo) / Dominate ($15K+$3.5K/mo)

Type a template name, or press enter for default.
```

---

## Step 8: Generate Proposal

Read all three JSON files from `output/`.
Read agency config and selected pricing template.

**Synthesize recommendations:** map audit findings and opportunity signals to agency services. Prioritize by impact: conversion and revenue first, then SEO, then aesthetics.

**Generate executive summary:** 3-4 sentences. What was found, why it matters, what you recommend. Reference specific scores.

**Build the competitive comparison:** Using the `prospect_signals` and `competitors[].signals` data from `output/prospect-research.json`, generate:

- `{{ competitive_intro }}` — 1-2 sentences: "Here's how [CLIENT_NAME] compares to [N] local competitors on key digital presence indicators."
- `{{ competitor_headers }}` — `<th>` elements for each competitor name
- `{{ competitive_rows }}` — table rows for each feature. Use `<span class="comp-icon-yes">&#10003;</span>` for present, `<span class="comp-icon-no">&#10007;</span>` for missing. Features to compare:
  - HTTPS / SSL
  - Meta descriptions
  - Schema markup
  - Mobile-friendly
  - Google Business Profile
  - Social media presence
  - Online booking
  - Contact form
  - Clear CTA above fold
- `{{ competitive_summary }}` — 2-3 sentences summarizing where the prospect falls behind competitors and what that means for their business. Be specific: "2 of 3 competitors have online booking. [CLIENT_NAME] does not, which means potential customers have an easier path to convert with competitors."

**Build the HTML proposal:** Read `templates/proposal.html`. Replace all `{{ }}` tokens with generated content:

- Cover: agency name, client name, date, tagline
- Executive summary
- Brand audit: score cards, voice details, visual details, SEO table, tech checks, conversion signals
- Performance audit: Lighthouse scores, Core Web Vitals, top issues
- Competitive comparison: prospect vs competitors feature table
- Recommendations: prioritized action items tagged with services
- Pricing: tier cards from selected template
- Next steps: agency contact info

Create filename slug from client name (lowercase, hyphens, no special chars).

Write:
- `output/proposal-[slug].html`
- `output/proposal-[slug].md` (markdown version)

**Generate PDF:**
```
python3 scripts/generate_pdf.py output/proposal-[slug].html output/proposal-[slug].pdf
```

Open the PDF: `open output/proposal-[slug].pdf`

---

## Step 9: Generate Sales Brief

Using data already collected from prospect research, brand audit, and Lighthouse, generate an internal sales document. This is NOT for the client. It's for the person making the call.

Write to `output/brief-[slug].md`:

```markdown
# Sales Brief: [CLIENT_NAME]
**Generated:** [date] | **Category:** [industry] | **Location:** [location]

---

## Contact Information

- **Business:** [name]
- **Website:** [url]
- **Phone:** [phone number if found during research]
- **Email:** [email if found on contact page or website]
- **Address:** [physical address if found]
- **Decision maker:** [owner/manager name if found during research, or "not identified"]
- **Best contact method:** [recommend based on what's available: phone if listed prominently, email if contact form only, walk-in if local with address]

## Internal Briefing

### What they do
[1-2 sentences from prospect research: industry, services, target market]

### What's working
[2-3 bullet points from brand audit strengths. Lead with positives so the call doesn't feel like an attack.]

### Key pain points (use these in the call)
[3-5 bullet points derived from opportunity signals and audit findings. Be specific:]
- [e.g., "Site has no meta descriptions on any page. They're invisible to Google for local searches."]
- [e.g., "No online booking. Every competitor in the area has it."]
- [e.g., "Lighthouse performance score is 38. Site takes 6+ seconds to load on mobile."]
- [e.g., "No Google Business Profile found. Missing the #1 free local marketing channel."]

### Competitive context
[1-2 sentences about how they compare to local competitors found during research]

### Recommended service package
[Template name and recommended tier based on the gaps found. Brief justification: "Their biggest issues are performance and SEO, which the Growth tier covers."]

## Call Script

### Opening (15 seconds)
"Hi, is this [decision maker / the owner]? My name is [YOUR NAME] from [AGENCY NAME]. I was looking at local [industry] businesses in [location] and came across [BUSINESS NAME]. I noticed a few things on your website that might be costing you customers. Do you have two minutes?"

### If they say yes: Lead with value (30 seconds)
"I ran a quick audit on [website]. A couple things stood out:

[Pick the top 2 pain points. Frame as lost revenue, not technical problems:]
- [e.g., "Your site takes about 6 seconds to load on a phone. Google's data shows that 53% of mobile visitors leave if a page takes more than 3 seconds. That's real traffic you're losing."]
- [e.g., "When someone searches '[industry] in [location],' your site isn't showing up with a description. Your competitors are. That means they're getting the click, not you."]

I put together a short report that breaks all of this down. No cost, no obligation. Can I send it over?"

### If they want more detail
"The report covers four areas: how your brand comes across online, your site's technical performance, your SEO visibility, and how well your site converts visitors into leads. Each one is scored and I've included specific recommendations."

### If they ask about cost
"The audit itself is free. If you want help implementing the fixes, I can walk you through some options. Our [RECOMMENDED TIER] package at $[PRICE] covers the main issues I found, but there's no pressure. The report is useful on its own."

### Objection handling
- **"I'm happy with my website":** "That's great. The report might confirm that. Either way, it's worth a look. I found [X specific issue] that could be a quick fix."
- **"I don't have budget right now":** "No problem. The report is free and the recommendations don't expire. When you're ready to invest, you'll have a clear priority list."
- **"Send me an email":** "Absolutely. What's the best email? I'll send the report over today."
- **"Not interested":** "No worries. Thanks for your time."

### Close
"I'll send that report over to [email]. It'll have everything we talked about plus the specific numbers. If anything catches your eye, just reply and we can set up a quick call. Sound good?"
```

---

## Step 10: Generate Follow-up Email

Write a ready-to-send follow-up email to `output/email-[slug].md`. This is the email the user sends after the call (or instead of a call if email is the only contact method).

Use data from the prospect research, brand audit, and Lighthouse to personalize every line. No generic filler.

```markdown
**Subject:** Quick audit of [BUSINESS NAME]'s website — a few things you should see

---

Hi [DECISION MAKER NAME or "there"],

[YOUR NAME] from [AGENCY NAME]. [If call happened: "Thanks for taking my call earlier." If no call: "I came across [BUSINESS NAME] while researching [industry] businesses in [location]."]

I ran a quick audit on [website URL] and found a few things worth looking at:

- **[Pain point 1, framed as impact]** — [e.g., "Your site takes about 6 seconds to load on mobile. Google's research shows over half of visitors leave after 3 seconds, so this is likely costing you traffic."]
- **[Pain point 2, framed as impact]** — [e.g., "None of your pages have meta descriptions. This means Google is choosing what to show in search results, and it's not always flattering."]
- **[Pain point 3, framed as opportunity]** — [e.g., "Your competitors in the area have online booking set up. Adding this alone could capture leads you're currently losing."]

I put together a full report covering your brand presence, site performance, SEO, and conversion signals. It's attached.

[If pricing was discussed: "I also included a few options for fixing the issues I found, starting at $[LOWEST TIER PRICE]."]

No pressure at all. The report is yours either way. If anything stands out and you want to talk through it, just reply to this email or grab a time here: [AGENCY WEBSITE or BOOKING LINK].

[YOUR NAME]
[AGENCY NAME]
[AGENCY PHONE]
[AGENCY EMAIL]
```

---

## Step 11: Deliver

Display a step-by-step action plan so the user knows exactly what to do next:

```
Everything is ready for [CLIENT_NAME].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR FILES:
1. output/brief-[slug].md          ← Read this first (contact info + call script)
2. output/email-[slug].md          ← Copy/paste into your email client
3. output/proposal-[slug].pdf      ← Attach this to the email
4. output/proposal-[slug].html     ← Or send this link if hosted

YOUR NEXT STEPS:
1. Open brief-[slug].md and review the contact info and call script
2. Call [CLIENT_NAME] at [phone if found] using the script in the brief
3. After the call, open email-[slug].md and copy it into your email client
4. Attach proposal-[slug].pdf and hit send
5. Follow up in 3 days if no response

AUDIT SNAPSHOT:
Brand: Voice [rating], Visual [rating], SEO [rating], Conversion [rating]
Lighthouse: Performance [score], Accessibility [score], SEO [score]
Signals: [count] opportunity gaps identified
Package: [template name] — [recommended tier] at $[price]
```

---

## Voice & Style

- Direct, no preamble. Progress updates are brief.
- Between steps, only display essential status. Do not narrate what you're about to do at length.
- The user should feel like they're making quick decisions while the system does the heavy lifting.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT hedge.

## Error Handling

- **Config missing:** "Run `/setup` first." Stop.
- **WeasyPrint missing:** "Run `pip install -r requirements.txt`." Stop.
- **No prospects found:** "No businesses found for that category. Try a different search." Return to Step 1.
- **Lighthouse fails:** Skip performance section. Continue.
- **WebFetch fails on prospect:** Remove from list. If fewer than 2 remain, expand search.
- **PDF generation fails:** Display error. Note HTML version is available.

## What This Skill Does NOT Do

- Does not send the proposal or contact the prospect
- Does not create accounts or authenticate with external services
- Does not spawn subagents or teams
- Does not modify agency config or pricing templates
- Does not require any API keys beyond what Claude Code and the system provide
