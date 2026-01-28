# Categorization Plan

> **Purpose:** Define how categories, deterministic rules, confidence scoring, and review workflows operate in a multi-tenant environment so users understand governance before implementation.

## 1. Category Inventory Strategy
- **Default Set:** Provide a global starter taxonomy (below) enabled for every workspace by default.
- **Workspace Extensions:** Allow admins to clone the default set and add custom slugs under their workspace namespace (`custom.*`).
- **Versioning:** Track category versions per workspace so historical transactions retain their original label even if definitions change.
- **Retirement:** Categories can be soft-deleted; legacy transactions remain readable but new assignments are blocked.

### 1.1 Default Categories (v0)
| Category | Definition |
| --- | --- |
| `income.salary` | Net payroll deposits and employer reimbursements. |
| `income.other` | Miscellaneous credits such as gifts, refunds, or interest. |
| `housing.rent` | Rent, mortgage, HOA dues. |
| `utilities.core` | Electricity, water, gas, trash services. |
| `utilities.connectivity` | Internet, mobile phone, streaming infrastructure. |
| `transportation.fuel` | Gasoline, EV charging, fuel stations. |
| `transportation.services` | Rideshare, public transit, parking, tolls. |
| `food.groceries` | Supermarkets and meal kit subscriptions. |
| `food.dining` | Restaurants, cafes, delivery services. |
| `health.insurance` | Premiums for medical, dental, vision plans. |
| `health.out_of_pocket` | Pharmacies, clinics, medical supplies. |
| `savings.investment` | Transfers to brokerage, IRA, or HSA accounts. |
| `lifestyle.shopping` | Retail purchases, apparel, household goods. |
| `lifestyle.entertainment` | Subscriptions, events, recreation. |
| `uncategorized.review` | Placeholder for transactions awaiting manual classification. |


## 2. Role-Based Responsibilities
| Role | Capabilities related to categorization |
| --- | --- |
| Admin | Manage category inventory, create/approve rules, force overrides, assign reviewers. |
| Reviewer | Draft rules, resolve review queues, submit manual overrides for approval. |
| Viewer | Read-only access to categories and review status; cannot change rules. |

Roles are assigned per workspace via `workspace_memberships`. Privileges map directly to the APIs/CLI commands exposed.

## 3. Rules-First Pipeline
1. **Normalization Stage (ingest time):**
   - Uppercase, trim, collapse whitespace, strip institution-specific prefixes.
   - Persist normalized form plus normalization metadata for audit.
2. **Rule Evaluation (priority queue):**
   - `exact_match` (priority 1000) → deterministic IDs/memos.
   - `keyword_regex` (priority 750) → regex/keyword combos with optional capture groups.
   - `amount_context` (priority 500) → amount windows + merchant cues.
   - `fallback` rules (priority 100) → catch-all heuristics.
3. **Execution Model:** Stop at first definitive match; ambiguous matches store candidate list in `metadata.candidate_categories` and raise `needs_review`.
4. **Governance:** Every rule records `workspace_id`, `owner_user_id`, `status` (draft, active, retired), `version`, `expected_precision`, and optional expiration date.

### 3.1 Rule Lifecycle
- Draft → Active: requires admin approval if created by reviewer.
- Active → Retired: admin-only; transactions keep historical category.
- Promotion: manual overrides hitting threshold (e.g., ≥5 identical overrides) surface as suggested rules in the rule queue.

## 4. Confidence Handling
- **Default weights:** `exact_match = 0.95`, `keyword_regex = 0.8`, `amount_context = 0.7`, `fallback = 0.5`.
- **Aggregation:** Combine agreeing signals using capped sum: $confidence = \min(1, \sum weights)$.
- **Thresholds:** Workspace-level setting (default 0.7). Transactions below threshold route to review even if categorized.
- **Calibration:** Regularly compare confidence vs actual corrections to adjust weights per workspace. Store calibration runs in audit log.

## 5. Needs-Review Workflow
- **Triggers:** low confidence, conflicting rules, provisional rule hit, parser warning, or manual flag by a user.
- **Queue Ownership:** Reviewers see workspace-specific queues; admins can reassign or bulk-close.
- **States:** `open` → `assigned` → `resolved` (with resolution note). All transitions recorded in `audit_events`.
- **Notifications:** Optional email/Slack hooks per workspace when queue exceeds threshold.

## 6. Manual Corrections & Overrides
1. Reviewer/Admin edits category via CLI (`categorize override --id ...`) or UI.
2. System logs `manual_override` event with actor, old/new category, reasoning, related rule (if any), and fingerprint.
3. Override persists as highest-priority rule scoped to `ingest_fingerprint` until promoted or dismissed.
4. Admins review override suggestions weekly; accepted overrides become generalized rules, declined overrides expire after configurable window.

## 7. Collaboration & Audit
- Every rule change, override, and review action emits an `audit_event` with signature/hash for tamper evidence.
- Provide `categorization history` command/API showing timeline per transaction (rules fired, overrides, reviewer notes).
- Maintain reviewer assignment logs for accountability.

## 8. Open Questions / TODOs
- Decide on UI/CLI surfaces for drafting vs approving rules.
- Define SLA for review queue processing (e.g., 24h).
- Determine how category translations/localizations will work (if needed).
- Establish retention policy for inactive rules and overrides.

