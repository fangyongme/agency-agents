# Factory acquisition runbook

## 1. Start and resume

Use a campaign ID such as `pilot-001`. Read the private factory profile, existing
campaign files and `work/pipeline.json`. A blank template contains no performance
history. Inventory available search, document, media and communication tools;
use only those actually connected and authorized. No paid data service is
required. Without web access, work from supplied sources and mark research gaps.

The profile starts with known broad positioning. Before product-specific content,
need approved product names, catalog/application evidence and real assets. Before
actual first contact, need real sender identity, selected market, verified buyer
and usable business contact. Before a quote, need the approved internal quote
record. Missing one input blocks only the dependent stage.

## 2. Ordered handoffs

| Step | Owner | Required input | Output | Exit condition / next step |
| --- | --- | --- | --- | --- |
| 1 Customer research | Outbound Strategist | profile, market request, sources | research.md | sourced ICP and buyer questions -> 2 |
| 2 Content production | Social Media Strategist | research, catalog facts, assets | content-brief.md; linkedin.md | claim map and master script -> 3 |
| 3 Channel adaptation | Video Optimization Specialist | master brief and source assets | video-pack.md | TikTok, Instagram, YouTube sections -> 4 |
| 4 Asset review | Social Media Strategist; coordinator | all four channel packages | review.md; publication records | actual assets and claims reviewed; authorization needed for publishing |
| 5 B2B qualification | Outbound Strategist | ICP, candidate sources, existing buyers | qualification.json | score plus hard gates -> 6 |
| 6 First contact | Sales Outreach; coordinator | qualified buyer, evidence, history | outreach/<buyer-id>.md | verified recipient + approved final revision + authorized execution |
| 7 RFQ follow-up | Sales Outreach; factory quoting owner | actual inquiry and approved catalog/quote | rfq/<rfq-id>.json; reply draft | clarify -> product match review -> approved quote -> authorized reply |
| 8 Review | Social Media Strategist; coordinator | confirmed publication and buyer events | review.md update | one evidence-based improvement for next cycle |

Qualification can proceed after step 1 while content is produced; external
publication is not required before responding to a real RFQ. Inbound buyers go
directly to identity/product checks and step 7. The main session is the
coordinator, not a fifth installed agent.

## 3. B2B qualification rubric

These weights are editable pilot heuristics, not validated conversion predictors.

| Dimension | 0 | 10 | 20 |
| --- | --- | --- | --- |
| Business model | unknown / consumer only | mixed retail and trade evidence | confirmed importer / wholesaler / distributor |
| Product relevance | unknown / unrelated | adjacent hydraulic/brake parts | explicit relevant cylinder range |
| Vehicle application | unknown / mismatch | broad Asian applications | catalog evidence matching supported vehicle groups |
| Market fit | unknown / not selected | market plausible but servicing unconfirmed | selected market and factory servicing confirmed |
| Contact evidence | none / unverified | company-level business inbox verified | relevant purchasing role and destination verified |

For outbound: at least 70/100, verified business identity, direct relevant-product
evidence, selected serviceable market, verified business destination, resolved
duplicates and no suppression are all required. Score is necessary but not
sufficient. An adjacent-only seller stays in research until relevance is shown.
Public catalog listings indicate fit, not an active purchase request. Never use
nationality, religion or other sensitive personal attributes as scoring factors.

Company identity: prefer a canonical company domain; without one use verified
legal/trading name + country and mark confidence. Normalize tracking parameters
and known domain aliases without merging different companies by name alone.
Retain aliases and platforms under a stable `B0001`-style buyer ID. Multiple
people at one company are contacts within the same account, not new buyers.

## 4. State and evidence

- Buyer: `research_needed` -> `qualified` -> `draft_ready` -> `contacted`
  -> `replied`. `suppressed` / `disqualified` are explicit states; any refusal
  stops outbound immediately. An inbound buyer may start at `replied` with proof.
- RFQ: `received` -> `needs_clarification` or `product_review` ->
  `ready_for_quote` -> `quote_approved` -> `quote_sent` -> `awaiting_buyer` ->
  `sample_confirmed` / `order_confirmed` / `lost`. A sample is optional; loss
  may occur earlier. Price approval and message delivery must be separate events.
- Content: `draft` -> `blocked_assets` or `review_ready` -> `approved` ->
  `published`. Approval is scoped to exact content/asset revision. Publishing
  needs a receipt/URL; failure leaves the stage unchanged with an error event.

Use the structures in `templates/pipeline.json` and `templates/rfq.json`. Copy
empty arrays into the operational pipeline, not placeholder example records.
Every event has ID, UTC timestamp, owner, source/receipt, from/to stage and
next action. Track a timezone with any scheduled proposal. `next_action_at` is
a reminder proposal unless an actual scheduler is separately configured.

Approvals record actor, time, scope, target, revision and evidence of user
authorization. The agent must not create approval evidence on the user's behalf.
For a scoped batch approval, reuse it only while targets/content remain in scope.
Record attempted actions and tool errors separately from successful delivery.

## 5. Product and quotation contract

An RFQ must preserve raw OE, raw quantity/unit, original language and row location.
Approved normalization removes formatting only; truncated/OCR-ambiguous numbers
stay candidates. Human product confirmation is required for uncertain or multiple
matches. Preserve rejected/unquoted lines, reasons and original ordering.

The internal system (or quoting person) receives `rfq_id`, source row, normalized
OE, quantity/unit, candidate/confirmed SKU, destination and uncertainty flags.
It returns a dated quote ID/version with approved price, currency, price unit,
MOQ, available terms, validity and approver evidence. Catalog fit and commercial
approval are independent. Partial quotes identify each missing line and never
silently delete an unrecognized product. The reply follows the buyer's original
table where feasible and keeps an internal audit copy.

## 6. Production and measurement

The four requested platforms are the active scope. Do not automatically add
Facebook, WhatsApp Status or other channels from an older calendar. Existing
approved cadence can be imported; otherwise propose two master topics for the
first week, reused across channels according to capacity. This is not a fixed
posting requirement. Never reset completed records when importing an older plan.

Use 24h for technical checks, 72h for an early read, and a complete 168h window
for comparable results. Store raw platform metrics separately; average watch
duration divided by length is not completion rate. Unknown values stay null.

| Metric | Definition |
| --- | --- |
| Unique buyers | distinct buyer IDs, across all channels |
| Qualified RFQs | actual RFQs with target business identity + country/market + identifiable supported need + quantity |
| Valid quotations | RFQs with an approved dated quote record; report issued/sent separately |
| Reply rate | unique buyers with replies / unique buyers with successfully delivered first contacts |
| Qualified-RFQ rate | unique contacted buyers with qualified RFQs / unique buyers with delivered first contacts; inbound reported separately |
| Orders | actual order confirmations; payment tracked separately |

When denominator is zero, report `N/A`, not zero percent. Preserve first known
source for attribution; use `unknown` where evidence is missing. Count an RFQ
once per RFQ ID and distinguish this from unique RFQ buyers. No follower or
inquiry guarantees. Repeat the cycle only from measured results.

## 7. Ready-to-use prompts

**Bootstrap**

> Read AGENTS.md and the factory profile. Inventory missing facts and tools.
> Create campaign pilot-001. Have Outbound Strategist prepare sourced customer
> research from the supplied market request. Do not invent leads if sources are
> unavailable. Then have Social Media Strategist produce one master brief and
> LinkedIn draft, followed by Video Optimization Specialist's three-channel pack.
> Return drafts, input gaps and exact handoffs; no external publication or sending.

**Qualify and draft**

> Use Outbound Strategist to qualify the supplied companies against the current
> profile and pipeline. For eligible, nonduplicate buyers, use Sales Outreach to
> write first-contact drafts with verified recipients. Give me the review queue.

**Handle inquiry**

> Use Sales Outreach to process the attached inquiry. Preserve original rows and
> raw OE values. Match only against the supplied approved catalog; send uncertain
> candidates to product review. Prepare the internal quotation handoff and the
> buyer clarification draft. Do not invent price or mark a quote as sent.
