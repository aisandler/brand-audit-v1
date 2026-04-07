# Lighthouse Audit

*Runs a Lighthouse performance audit and produces a structured report with scores, Core Web Vitals, and prioritized issues.*

---

## Trigger

User runs `/lighthouse-audit` and provides a website URL (either as an argument or when prompted).

## Input

If no URL is provided in the arguments, ask:

```
What URL should I audit? Drop it and I'll run Lighthouse.
```

Store as `SITE_URL`. Ensure it has a protocol (default to `https://`).

Check for `--save-json` flag in the arguments.

---

## Phase 1: Pre-flight Check (5 seconds)

Run `which google-chrome || which chromium || which chromium-browser` via Bash to verify Chrome is available.

If Chrome is not found:
"Lighthouse requires Chrome or Chromium. Install it first:
- macOS: Chrome is usually at /Applications/Google Chrome.app
- Linux: `sudo apt install chromium-browser`
- Or install Chrome from https://google.com/chrome"

Then stop.

---

## Phase 2: Run Lighthouse (30-60 seconds)

Tell the user: "Running Lighthouse on [URL]. This takes 30-60 seconds."

Run via Bash:

```
npx lighthouse SITE_URL --output=json --output-path=stdout --chrome-flags="--headless=new --no-sandbox" --only-categories=performance,accessibility,best-practices,seo 2>/dev/null
```

Capture the full JSON output.

If the command fails:
- If error mentions Chrome: "Lighthouse couldn't find Chrome. Make sure Chrome or Chromium is installed and accessible."
- If error mentions the URL: "Lighthouse couldn't reach that URL. Check that the site is live and publicly accessible."
- For other errors: display the error message.

---

## Phase 3: Parse Results

From the Lighthouse JSON output, extract:

**Category Scores** (multiply by 100 for percentage):
- Performance
- Accessibility
- Best Practices
- SEO

Map scores to ratings:
- 90-100: Strong
- 50-89: Adequate
- 0-49: Weak

**Core Web Vitals** from `audits`:
- First Contentful Paint (FCP): `audits.first-contentful-paint.numericValue` (convert to seconds)
- Largest Contentful Paint (LCP): `audits.largest-contentful-paint.numericValue` (convert to seconds)
- Total Blocking Time (TBT): `audits.total-blocking-time.numericValue` (keep as ms)
- Cumulative Layout Shift (CLS): `audits.cumulative-layout-shift.numericValue`
- Speed Index: `audits.speed-index.numericValue` (convert to seconds)

**Top Issues** -- For each category scoring below 90, extract the top 3 failing audits:
- Look at `categories.[category].auditRefs` for audits with `weight > 0`
- Cross-reference with `audits.[id]` where `score < 1`
- Extract: audit title, description (first sentence only), and savings estimate if available (from `audits.[id].details.overallSavingsMs` or `overallSavingsBytes`)

---

## Phase 4: JSON Export (conditional)

If `--save-json` was passed OR this was invoked as part of `/proposal`:

1. Create `output/` directory if it doesn't exist (via Bash: `mkdir -p output`)
2. Write results to `output/lighthouse-audit.json` with structure:

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
    {
      "category": "performance",
      "title": "...",
      "description": "...",
      "savings": "..."
    }
  ]
}
```

---

## Phase 5: Output

Display the report in chat:

```markdown
# Lighthouse Audit: [domain]

**Scanned:** [URL] | [date]

---

## Scores

| Category | Score | Rating |
|----------|-------|--------|
| Performance | [score] | [Strong/Adequate/Weak] |
| Accessibility | [score] | [Strong/Adequate/Weak] |
| Best Practices | [score] | [Strong/Adequate/Weak] |
| SEO | [score] | [Strong/Adequate/Weak] |

## Core Web Vitals

| Metric | Value | Status |
|--------|-------|--------|
| First Contentful Paint | [X.Xs] | [good/needs improvement/poor] |
| Largest Contentful Paint | [X.Xs] | [good/needs improvement/poor] |
| Total Blocking Time | [Xms] | [good/needs improvement/poor] |
| Cumulative Layout Shift | [X.XX] | [good/needs improvement/poor] |
| Speed Index | [X.Xs] | [good/needs improvement/poor] |

Core Web Vitals thresholds: FCP good <1.8s, LCP good <2.5s, TBT good <200ms, CLS good <0.1, SI good <3.4s.

## Top Issues

1. **[audit title]** -- [description] -- [savings estimate if available]
2. ...
3. ...
```

---

## Voice & Style Rules

Same as brand-audit:
- Direct, no preamble. Lead with findings, not methodology.
- Use concrete language: cite specific scores, name specific audits.
- No corporate filler.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT hedge: say "the performance score is 42" not "the performance score could potentially be improved."

## Error Handling

- If Lighthouse fails entirely: display the error and stop. Do not fabricate scores.
- If a specific category is missing from output: note "not available" for that category.
- If Core Web Vitals metrics are missing: note "not measured" for those metrics.

## What This Skill Does NOT Do

- Does not modify any project files (unless --save-json is passed)
- Does not provide recommendations beyond what Lighthouse reports
- Does not run accessibility fixes
- Does not require any API keys beyond what's on the system
- Does not spawn subagents or teams
