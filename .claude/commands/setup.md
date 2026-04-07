# Agency Setup

*First-run onboarding. Configures your agency profile, services, and pricing so all skills have the context they need.*

---

## Trigger

User runs `/setup`. No arguments needed.

## Pre-flight

Check if `config/agency-config.json` already exists by reading the file.

- If it exists: display the current agency name and ask "You already have a profile configured for **[agency name]**. Want to update it or start fresh?" If they choose update, pre-fill existing values as defaults. If start fresh, proceed as if new.
- If it does not exist: proceed with onboarding.

---

## Phase 1: Collect Agency Details

Ask for the following using AskUserQuestion, one group at a time. Do not dump all questions at once.

**Group 1: Identity**
- Agency name (required)
- Contact email (required)
- Phone number (optional)
- Website URL (optional)
- Tagline or one-liner (optional, e.g., "Websites that work as hard as you do")

**Group 2: Brand**
- Primary brand color (hex code, default `#3B82F6`)
- Secondary brand color (hex code, default `#08080C`)
- Heading font (default `Instrument Serif`)
- Body font (default `DM Sans`)

If the user says "use defaults" or similar, apply all defaults and move on.

**Group 3: Services**

Present as a list. Ask which they offer:
1. Web Design
2. SEO
3. Content Marketing
4. Social Media Management
5. Paid Advertising
6. Email Marketing
7. Branding / Brand Strategy

Store selected services as lowercase kebab-case: `web-design`, `seo`, `content-marketing`, `social-media`, `paid-ads`, `email-marketing`, `branding`.

**Group 4: Pricing**

List the available pricing templates:
1. **Website Redesign** — Starter / Growth / Premium tiers for site builds
2. **Monthly Retainer** — Essentials / Growth / Scale tiers for ongoing services
3. **One-Time Audit** — Single-tier comprehensive digital audit
4. **Hybrid** — Website project + monthly retainer bundle

Ask which template to use as their default. They can always override per-proposal.

After selection, display the tier names and prices from the selected template file in `config/pricing-templates/`. Ask if they want to customize any prices or line items. If yes, collect overrides. If no, move on.

**Group 5: Market Focus**
- Target verticals (e.g., "restaurants, dental practices, law firms")
- Geographic focus (city, region, or "national")

---

## Phase 2: Write Config

Create the `config/` directory if it doesn't exist.

Write `config/agency-config.json` with this structure:

```json
{
  "agency": {
    "name": "Acme Digital",
    "email": "hello@acmedigital.com",
    "phone": "555-0100",
    "website": "https://acmedigital.com",
    "tagline": "Websites that work as hard as you do",
    "brand": {
      "primary_color": "#3B82F6",
      "secondary_color": "#08080C",
      "font_heading": "Instrument Serif",
      "font_body": "DM Sans"
    }
  },
  "services": ["web-design", "seo", "content-marketing"],
  "pricing_template": "website-redesign",
  "pricing_overrides": {},
  "target_verticals": ["restaurants", "dental"],
  "geographic_focus": "Austin, TX"
}
```

Omit fields the user left blank (phone, website, tagline). Do not include null values.

---

## Phase 3: Update CLAUDE.md

Read the current `CLAUDE.md`. Append (or replace if it already exists) an `## Agency Profile` section:

```markdown
## Agency Profile

- **Agency:** [name]
- **Services:** [comma-separated list]
- **Pricing:** [template name] as default
- **Market:** [verticals] in [geographic focus]
- **Config:** config/agency-config.json
```

This gives all skills ambient context about the agency without needing to read the config file every time.

---

## Phase 4: Confirm

Display:

```
Setup complete.

Agency: [name]
Services: [list]
Default pricing: [template name]
Market: [verticals] in [location]

Config saved to config/agency-config.json

Next steps:
- Run /brand-audit <url> to audit a prospect's site
- Run /lighthouse-audit <url> for a performance report
- Run /prospect-research <business name> for a business dossier
- Run /proposal <url> to generate a full proposal package
```

---

## Voice & Style

- Conversational but efficient. Don't over-explain each field.
- Use sensible defaults. Don't make the user think about things that have obvious answers.
- If the user gives terse answers, accept them. Don't ask for confirmation on every field.
- Do NOT use em-dashes. Use periods, commas, or colons.
- Do NOT hedge or add filler language.

## What This Skill Does NOT Do

- Does not create accounts or authenticate with external services
- Does not send any data externally
- Does not modify any files outside of `config/agency-config.json` and `CLAUDE.md`
- Does not require any API keys
