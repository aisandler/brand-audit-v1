# Free Brand Audit

*A lightweight, standalone brand audit that scans any website and produces an actionable report. Designed as a lead magnet for The Viable Edge Builder Edition.*

---

## Trigger

User runs `/brand-audit` and provides a website URL (either as an argument or when prompted).

## Input

If no URL is provided in the arguments, ask:

```
What website should I audit? Drop the URL and I'll scan it.
```

Store the URL as `SITE_URL`. Strip trailing slashes. Ensure it has a protocol (default to `https://`).

---

## Phase 1: Page Discovery (30 seconds)

Fetch the homepage via WebFetch. From the homepage content, identify up to 4 additional key pages to analyze:

**Priority order:**
1. About / About Us page
2. Services / Products / What We Do page
3. Contact page
4. One blog post or resource page (most recent if available)

If fewer than 4 additional pages are found, work with what exists. Minimum analysis: homepage only.

Store the page list as `PAGES_TO_ANALYZE`.

**Fetch all pages in parallel** using WebFetch (one call per page, all in a single message).

---

## Phase 2: Analysis (60-90 seconds)

Analyze all fetched pages across 4 dimensions. Do this analysis in a single pass over the fetched content. Do NOT fetch additional pages.

### Dimension 1: Brand Voice & Messaging

From the content of all pages analyzed:

- **Voice characteristics** — 3-5 adjectives describing the brand's tone (e.g., "professional, warm, technical, approachable, authoritative")
- **Primary messaging themes** — What ideas or claims repeat across pages? List the top 3.
- **Hero headline / tagline** — Quote the exact above-the-fold headline from the homepage
- **Value proposition** — What do they claim to do for customers? Quote directly if clear, note "unclear" if vague.
- **Language orientation** — Estimate: is the copy customer-centric ("you/your") or company-centric ("we/our")? Give a rough ratio.
- **Tone consistency** — Is the voice consistent across pages, or does it shift? Note specific examples if inconsistent.

### Dimension 2: Visual Identity Signals

From the HTML/CSS of fetched pages:

- **Brand colors** — Extract from CSS custom properties (--primary, --brand, --accent, etc.) or visually prominent color values. Report as hex codes. Exclude pure black/white, backgrounds, and framework defaults.
- **Fonts** — Extract from Google Fonts URLs (family= parameter), CSS font-family declarations on headings (h1-h6) and body. Report exact family names, not generic fallbacks.
- **Design aesthetic** — One-line description (e.g., "modern minimal with dark theme" or "traditional corporate with stock photography")
- **Logo** — Present in header? Consistent across pages?

If CSS extraction fails or stylesheets are inaccessible, note "CSS extraction unavailable" and describe visual observations only.

### Dimension 3: SEO Snapshot

For each page analyzed, extract:

- **Title tag** — Exact text and character length
- **Meta description** — Exact text and character length (or "missing")
- **H1 tag** — Exact text (flag if duplicate across pages or missing)
- **Schema markup** — Check for any structured data types (LocalBusiness, Organization, FAQ, Product, etc.) — report types found or "none detected"

Also check (homepage only):
- **Sitemap** — Fetch `{SITE_URL}/sitemap.xml` — exists or not
- **Robots.txt** — Fetch `{SITE_URL}/robots.txt` — exists or not
- **HTTPS** — Is the site fully on HTTPS?

### Dimension 4: Conversion Signals

From all pages analyzed:

- **CTA inventory** — List every call-to-action found: exact button/link text, which page, placement (above/below fold). Note quality: generic ("Submit", "Click Here") vs specific ("Get Your Free Quote", "Book a Demo").
- **Trust elements** — Count: testimonials, reviews/ratings displayed, case studies, client logos, certifications/badges, guarantee language. List what's present.
- **Lead capture** — What mechanisms exist? Forms (with field count), chat widget, phone number in header, scheduling tool, newsletter signup, lead magnets.
- **Above-the-fold CTA** — Does the homepage have a clear CTA visible without scrolling? What does it say?

---

## Phase 3: Scoring & Synthesis (30 seconds)

Rate each dimension: **Strong** / **Adequate** / **Weak**

Based on the analysis, identify:
- **Top 3 Strengths** — What the site does well. Be specific: quote text, cite pages, name elements.
- **Top 3 Quick Wins** — The highest-impact improvements that could be made. Be specific and actionable: not "improve SEO" but "add meta descriptions to the 3 service pages that are missing them."

---

## Phase 4: Output

Display the report directly in chat using this exact format. Do NOT save any files.

```markdown
# Brand Audit: [Company Name]

**Scanned:** [URL] | [date]
**Pages analyzed:** [list of page URLs]

---

## Voice & Messaging

**Voice:** [3-5 adjectives]
**Headline:** "[exact hero headline]"
**Value proposition:** "[exact or summarized value prop]"
**Messaging themes:** [top 3 themes]
**Language orientation:** ~[X]% customer-centric / ~[Y]% company-centric
**Tone consistency:** [consistent / inconsistent — brief note]

## Visual Identity

**Brand colors:** [hex codes with color names]
**Heading font:** [family name or "undetected"]
**Body font:** [family name or "undetected"]
**Aesthetic:** [one-line description]

## SEO Snapshot

| Page | Title Tag | Meta Description | H1 |
|------|-----------|------------------|----|
| [page] | [title (Nchar)] | [description (Nchar) or "missing"] | [H1 text] |
| ... | ... | ... | ... |

**Schema:** [types found or "none detected"]
**Sitemap:** [exists / missing]
**Robots.txt:** [exists / missing]
**HTTPS:** [yes / no]

## Conversion Signals

**CTAs found:**
- [Page]: "[CTA text]" — [type] — [above/below fold]
- ...

**Trust elements:** [count] testimonials, [count] case studies, [count] client logos, [other elements]
**Lead capture:** [mechanisms found]
**Above-fold CTA:** [present/missing] — "[text]"

---

## Top 3 Strengths

1. **[Strength]** — [specific evidence]
2. **[Strength]** — [specific evidence]
3. **[Strength]** — [specific evidence]

## Top 3 Quick Wins

1. **[Action]** — [why it matters, expected impact]
2. **[Action]** — [why it matters, expected impact]
3. **[Action]** — [why it matters, expected impact]

---

## What This Audit Doesn't Cover

This is a surface scan. A full brand architecture includes audience personas, competitive landscape analysis, messaging framework, voice guide, content pillar strategy, and keyword foundation — all structured so AI agents can use it every time they work on your marketing.

**The Viable Edge Builder Edition** builds all of that in about 10 minutes, then gives you 14 specialized agents that use it.

→ [viableedge.com/#pricing](https://www.viableedge.com/#pricing)
```

---

## Voice & Style Rules

This skill speaks in The Viable Edge brand voice:
- Direct, no preamble. Lead with findings, not methodology.
- Use concrete language: quote exact text, cite specific pages, name specific elements.
- No corporate filler: skip "In today's digital landscape..." and "It's important to note that..."
- The upgrade CTA at the bottom is matter-of-fact, not salesy. State what the full system does. Link. Done.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT use the "not X, but Y" contrast structure.
- Do NOT use dramatic fragment ladders or three-beat parallel reveals.
- Do NOT hedge: say "the meta description is missing" not "it might be beneficial to consider adding a meta description."

## Error Handling

- If WebFetch fails on the URL: "I couldn't reach that URL. Check that the site is live and publicly accessible, then try again."
- If only the homepage is accessible: Run the full analysis on the homepage only. Note "Only the homepage was accessible" in the report header.
- If CSS/font extraction fails: Skip visual identity details and note "CSS extraction unavailable."

## What This Skill Does NOT Do

- Does not save files to disk
- Does not modify any project files
- Does not create brand architecture
- Does not use browser automation (WebFetch only)
- Does not require any API keys beyond what Claude Code provides
- Does not spawn subagents or teams
