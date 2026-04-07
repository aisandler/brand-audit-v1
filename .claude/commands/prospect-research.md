# Prospect Research

*Builds a business dossier on any prospect using web research. Designed for pre-proposal intelligence gathering.*

---

## Trigger

User runs `/prospect-research` and provides a business name, URL, or industry + location.

## Input

Parse the arguments to determine the mode:

- **URL provided** (contains `http` or `.com/.org/.net/etc`): Single-target mode using that URL.
- **Business name provided** (e.g., "Joe's Pizza Austin"): Single-target mode. Search for the business.
- **Industry + location** (e.g., "dentists in Portland"): Prospecting mode. Find 3-5 local businesses.

If no arguments provided, ask:

```
Who should I research? Give me one of:
- A business URL (e.g., https://joespizza.com)
- A business name and location (e.g., "Joe's Pizza Austin")
- An industry and location to find prospects (e.g., "dentists in Portland")
```

Check for `--save-json` flag in the arguments.

Read `config/agency-config.json` if it exists. Use `target_verticals` and `geographic_focus` for context-aware defaults when in prospecting mode.

---

## Single-Target Mode

### Phase 1: Web Research (60-90 seconds)

Run the following WebSearch queries in parallel (all in a single message):

1. `"[business name]" [location]` — general info
2. `site:linkedin.com/company "[business name]"` — LinkedIn profile
3. `"[business name]" reviews OR testimonials` — reputation signals
4. `"[business name]" competitors OR alternatives [industry]` — competitive landscape

If a URL was provided, also WebFetch the homepage to extract:
- Business name (from title tag or heading)
- Services/products listed
- Contact information
- Social media links (look for hrefs to facebook.com, instagram.com, linkedin.com, twitter.com/x.com, youtube.com)

From the search results, WebFetch the top 2-3 most relevant pages for detailed information.

### Phase 2: Compile Dossier

From all gathered information, compile:

**Business Overview:**
- Business name
- Industry/category
- Location (address if found)
- Website URL
- Years in business (if found)
- Size signals (employee count, location count, revenue indicators)

**Online Presence:**
- Google Business Profile: found or not found, rating, review count
- Social media: platforms found with follower/following counts if visible
- Directory listings: Yelp, BBB, industry-specific directories
- Website age/technology signals (if detectable from the homepage)

**Competitive Landscape:**
- 2-3 local competitors with URLs and brief notes
- How the prospect compares (stronger, weaker, similar)

**Opportunity Signals:**
Identify specific gaps that represent sales opportunities:
- Outdated or non-responsive website
- Missing or unclaimed Google Business Profile
- No social media presence or inactive accounts
- No SSL certificate
- Missing meta descriptions or poor SEO basics
- No online booking/scheduling
- Few or no reviews
- No clear call-to-action on website
- Missing contact form or lead capture

---

## Prospecting Mode

### Phase 1: Find Prospects (60-90 seconds)

Use the industry and location to run WebSearch queries:

1. `best [industry] in [location]`
2. `[industry] near [location]`
3. `top rated [industry] [location]`

If `config/agency-config.json` exists, cross-reference with `target_verticals` to confirm the industry is a match. Note if it's outside the configured verticals.

### Phase 2: Build Short Dossiers

For each of the top 3-5 businesses found:

WebFetch their homepage. Compile a brief dossier:
- Business name and URL
- Google rating and review count (from search results)
- One-line description of what they do
- 2-3 opportunity signals (from the list above)
- Prospect quality: Hot / Warm / Cold (based on number and severity of gaps)

---

## Phase 3: JSON Export (conditional)

If `--save-json` was passed OR invoked as part of `/proposal`:

1. Create `output/` directory if it doesn't exist (via Bash: `mkdir -p output`)
2. Write to `output/prospect-research.json`:

For single-target mode:
```json
{
  "mode": "single",
  "business_name": "...",
  "url": "...",
  "location": "...",
  "industry": "...",
  "date": "YYYY-MM-DD",
  "overview": {
    "years_in_business": null,
    "size_signals": "...",
    "description": "..."
  },
  "online_presence": {
    "google_business": { "found": true, "rating": 4.5, "review_count": 120 },
    "social_media": [{ "platform": "facebook", "url": "...", "followers": null }],
    "directories": ["yelp", "bbb"]
  },
  "competitors": [
    { "name": "...", "url": "...", "notes": "..." }
  ],
  "opportunity_signals": [
    "No SSL certificate",
    "Missing meta descriptions on all pages",
    "No Google Business Profile claimed"
  ]
}
```

For prospecting mode:
```json
{
  "mode": "prospecting",
  "industry": "...",
  "location": "...",
  "date": "YYYY-MM-DD",
  "prospects": [
    {
      "business_name": "...",
      "url": "...",
      "rating": 4.5,
      "review_count": 120,
      "description": "...",
      "opportunity_signals": ["...", "..."],
      "quality": "Hot"
    }
  ]
}
```

---

## Phase 4: Output

### Single-Target Output

```markdown
# Prospect Research: [Business Name]

**Location:** [city, state] | **Industry:** [category] | **Website:** [URL]

---

## Business Overview

[2-3 sentence summary: what they do, how long they've been around, size signals]

## Online Presence

- **Google Business:** [found/not found] — [rating] stars, [count] reviews
- **Facebook:** [URL or "not found"] — [followers if known]
- **Instagram:** [URL or "not found"] — [followers if known]
- **LinkedIn:** [URL or "not found"]
- **Other directories:** [Yelp, BBB, etc. or "none found"]

## Competitive Landscape

1. **[Competitor 1]** — [URL] — [one-line note]
2. **[Competitor 2]** — [URL] — [one-line note]
3. **[Competitor 3]** — [URL] — [one-line note]

## Opportunity Signals

1. **[Gap]** — [why it matters, what the fix looks like]
2. **[Gap]** — [why it matters, what the fix looks like]
3. **[Gap]** — [why it matters, what the fix looks like]
...
```

### Prospecting Output

```markdown
# Prospect Research: [Industry] in [Location]

**Found [N] prospects** | [date]

---

| Business | Rating | Reviews | Opportunity Signals | Quality |
|----------|--------|---------|---------------------|---------|
| [Name](URL) | [X.X] | [N] | [2-3 signals] | Hot/Warm/Cold |
| ... | ... | ... | ... | ... |

## Detailed Notes

### 1. [Business Name]
[2-3 sentences: what they do, key gaps, why they're a good prospect]

### 2. [Business Name]
...
```

---

## Voice & Style Rules

Same as brand-audit:
- Direct, no preamble. Lead with findings, not methodology.
- Use concrete language: name specific platforms, cite specific ratings, quote specific gaps.
- No corporate filler.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT hedge: say "no Google Business Profile found" not "there may be an opportunity to establish a Google Business Profile."
- Opportunity signals should be stated as facts, not suggestions.

## Error Handling

- If WebSearch returns no results: "I couldn't find information about that business. Check the spelling and try again, or provide a URL."
- If the URL is unreachable: "That URL isn't responding. Check that it's correct and the site is live."
- If in prospecting mode and fewer than 3 businesses found: report what was found. Don't pad with low-quality results.

## What This Skill Does NOT Do

- Does not contact the business
- Does not access paid databases or directories
- Does not scrape or gather facial images
- Does not save files to disk unless `--save-json` is passed
- Does not require any API keys beyond what Claude Code provides
- Does not spawn subagents or teams
