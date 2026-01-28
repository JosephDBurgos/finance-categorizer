# Data Model

> **Purpose:** Document the canonical, multi-tenant schema and supporting entities powering the finance categorizer so that design decisions are explicit before implementation.

## 1. Scope & Assumptions
- Deployment model (self-hosted vs managed): Managed (long-term) with Docker-based local dev/demo environment
- Tenancy model (workspace, household, organization): Multi-tenant, workspace-scoped with per-tenant isolation
- Storage technology assumptions (relational DB, append-only log, hybrid): Relational DB per workspace_id

## 2. Entity Overview
| Entity | Responsibility | Notes |
| --- | --- | --- |
| `workspaces` | Logical tenant boundary, encryption context, retention policy. | Capture key management + billing metadata. |
| `users` | Authenticated actor with MFA, roles, audit identity. | Include identity provider linkage. |
| `accounts` | Institution-specific feeds within a workspace. | Maps ingest artifacts to canonical transactions. |
| `transactions` | Canonical financial events normalized across institutions. | Includes categorization + review state. |
| `rules` | Deterministic categorization logic plus metadata. | Scoped per workspace; versioned. |
| `manual_overrides` | User corrections to categories/attributes. | Drives learning + replay. |
| `audit_events` | Append-only record of sensitive actions. | Backed by tamper-evident store if possible. |

_Add/delete rows as new entities surface._

## 3. Canonical Transaction Schema
| Field | Type | Description | Notes |
| --- | --- | --- | --- |
| `workspace_id` | UUID | Tenant owner; enforces row-level security. | Foreign key → `workspaces.id`. |
| `transaction_id` | UUIDv7 | Stable system identifier. | Generated on ingest. |
| `external_id` | string | Source-native identifier or hash. | Supports idempotency. |
| `owner_user_id` | UUID | User who imported/owns record. | Nullable for system ingests. |
| `occurred_at` | datetime (UTC) | Activity timestamp from institution. | Required. |
| `posted_at` | datetime (UTC, nullable) | Settlement timestamp. | Optional. |
| `amount` | decimal(18,4) | Signed amount (credit positive). | Currency stored separately. |
| `currency` | char(3) | ISO 4217 code. | No implicit conversions. |
| `description_raw` | text | Raw memo/description. | Immutable after ingest. |
| `description_clean` | text | Normalized description. | Document normalization rules. |
| `source_institution` | string | User-defined label. | Helps reporting. |
| `source_account` | string | Masked account id. | Combined unique per workspace. |
| `category` | string | Category slug. | Nullable until assigned. |
| `confidence` | decimal(3,2) | Range [0,1]. | Derived from rules. |
| `needs_review` | boolean | Flag for human attention. | Tied to workflow. |
| `sensitivity_level` | enum | Controls masking (e.g., payroll). | Values TBD. |
| `encryption_context` | string | Key reference or envelope id. | Enables per-tenant keys. |
| `metadata` | JSONB | Structured extras (fingerprints, warnings). | Avoid PII duplicates. |
| `created_at` | datetime | Record creation timestamp. | Auto-populated. |
| `updated_at` | datetime | Last mutation timestamp. | Tracks manual edits. |

### 3.1 Field Notes
- **Timestamps:** specify rounding/precision rules and how timezones are normalized.
- **Amounts & Currency:** document decimal precision, currency validation, and FX handling if conversions are added later.
- **Descriptions:** outline normalization pipeline + storage limits.
- **Security Columns:** explain how `sensitivity_level` and `encryption_context` drive masking and key selection.

## 4. Supporting Entities
### 4.1 Workspaces
- Key fields: `id`, `name`, `slug`, `primary_admin_user_id`, `encryption_key_arn`, `data_retention_days`, `created_at`.
- Decisions needed: provisioning flow, cross-workspace sharing (if any), deletion/archival policy.

### 4.2 Users & Memberships
- `users`: global identity record (id, email, MFA status, last_login).
- `workspace_memberships`: (workspace_id, user_id, role, invited_by, status, created_at).
- Outline role matrix (admin, reviewer, viewer) and how it maps to access control.

### 4.3 Accounts & Ingest Artifacts
- `accounts`: represent institution feeds with fields like `institution_name`, `account_mask`, `import_format`, `status`.
- `ingest_artifacts`: store metadata about uploaded files/APIs (checksum, size, storage_path, parsed_at, parser_version).
- Document relationship between artifacts and transactions.

### 4.4 Rules & Overrides
- `rules`: columns for `id`, `workspace_id`, `scope`, `priority`, `match_type`, `pattern`, `output_category`, `confidence_default`, `owner_user_id`, `enabled`, `version`, `created_at`.
- `manual_overrides` or `revision_log`: capture manual edits with `transaction_id`, `workspace_id`, `actor_user_id`, `field`, `old_value`, `new_value`, `reason`, `applied_at`.
- Capture how overrides graduate into canonical rules.

### 4.5 Audit Events
- Minimum columns: `id`, `workspace_id`, `actor_user_id`, `event_type`, `event_payload`, `created_at`, `signature`.
- Decide on retention and tamper-evident strategy (hash chains, external log, etc.).

## 5. Idempotency Strategy
1. Define `ingest_fingerprint` components (e.g., workspace_id + source_account + amount + occurred_at + normalized description).
2. Enforce uniqueness at DB level; describe conflict resolution when different users import overlapping data.
3. Detail replay flow: how to reprocess artifacts without duplicating transactions or losing manual edits.

## 6. Traceability & Auditability
- Describe event sourcing or change-data-capture approach for transactions and rules.
- Specify how `transaction history` queries are built (join transactions + overrides + audit events).
- Include plan for referencing raw artifacts (checksums, storage paths) from any transaction.

## 7. Access Control & Security Considerations
- Row-level security policy keyed on `workspace_id` and role.
- Fields requiring masking/encryption at query time (amounts, descriptions) depending on `sensitivity_level`.
- Logging requirements for read vs write operations.

## 8. Open Questions / TODOs
- Storage engine selection: PostgresSQL
- Encryption implementation details (KMS, libsodium, etc.): KMS (Start with Docker)
- Diagram/ERD ownership: _TODO_
- Performance targets (max transactions per workspace, expected ingest throughput): _TODO_

## 9. Iterative Build & Migration Plan
1. **Local Prototype (Now):**
	- Run PostgreSQL + app services via Docker Compose with sample workspaces and fake transactions.
	- Use application-layer encryption (libsodium/age) plus mock KMS IDs to exercise `encryption_context` without cloud costs.
	- Validate ingestion, categorization, manual overrides, and audit logging end-to-end using scripted fixtures.
2. **Portfolio Demo (Pre-Launch):**
	- Capture ERDs, CLI recordings, and docs showing multi-tenant flows; keep data synthetic.
	- Optionally publish read-only demo artifacts (screenshots, storyboards) without deploying a live service.
3. **Managed Pilot (Later):**
	- Migrate schema to managed PostgreSQL (e.g., RDS/Supabase) using migration tooling.
	- Integrate cloud KMS for per-workspace keys; rotate mock keys out.
	- Stand up hardened ingress (TLS, MFA) and invite pilot users; monitor cost/perf before scaling.
4. **Production Hardening (Optional):**
	- Add automated backups, retention enforcement, observability, and incident runbooks prior to onboarding external tenants.


