# Threat Model

> **Scope:** Multi-tenant finance categorizer with Docker-based local dev and managed production deployment. Threats are evaluated for both environments, emphasizing tenant isolation, rule governance, and data confidentiality.

## 1. Assets
- **Transaction Data:** Raw ingest files, canonical database rows, derived exports/reports per workspace.
- **Workspace Metadata:** Membership lists, role assignments, retention policies, encryption key references.
- **Categorization Logic:** Rule definitions, manual overrides, calibration metrics, confidence thresholds.
- **Audit Evidence:** `audit_events`, reviewer notes, calibration logs used for forensics/compliance.
- **Credentials & Secrets:** SSH keys, API tokens, CLI auth, mock KMS keys (dev) and real KMS keys (prod).
- **Execution Surface:** Local Docker stack, managed hosting environment, CI/CD pipelines, container images.

## 2. Entry Points
- **File Import Channels:** CLI uploads, watch folders, future UI upload forms; user-supplied CSV/OFX/QFX.
- **Categorization API (future):** REST/GraphQL endpoints for automation hooks and review queue actions.
- **CLI Commands:** `ingest`, `categorize`, `rules`, `review`, each accepting file paths, rule specs, or override payloads.
- **Rule/Override Management UI:** Interfaces where admins/reviewers create or approve rules and overrides.
- **Infrastructure Access:** SSH to dev host, container registries, managed DB consoles, KMS management consoles.

## 3. Threats
- **Data Leakage / Tenant Escape:** Misconfigured access controls or SQL bugs exposing one workspace’s data to another.
- **Malformed Inputs:** Crafted files exploiting parser bugs, causing buffer overflows, CSV injection, or rule bypass.
- **Unauthorized Access:** Credential theft (SSH, API tokens, MFA fatigue) leading to workspace takeover or key compromise.
- **Rule Poisoning & Override Abuse:** Malicious reviewers injecting exfiltration regex, low-confidence spam, or overrides that misclassify transactions for fraud.
- **Audit Log Tampering:** Attackers deleting or altering `audit_events` to hide activity.
- **Supply Chain Risks:** Compromised Docker image, dependency, or CI pipeline introducing backdoors.
- **Secrets Exposure:** Accidental commits or logs leaking real transactions, keys, or mock KMS identifiers.

## 4. Mitigations
- **Isolation Controls:** Per-row `workspace_id` enforcement, Postgres RLS policies, per-tenant encryption context, and mandatory MFA for admins.
- **Input Validation:** Schema + checksum validation, strict CSV parsers, size limits, sandboxed parsing workers with resource caps.
- **Least Privilege & Segregation:** Separate keys for dev/prod, scoped API tokens, role-based access to rule/override commands, short-lived credentials.
- **Change Control:** Rules/overrides managed via signed commits or approval workflow; calibration and rule lifecycle events logged to tamper-evident `audit_events`.
- **Data Hygiene:** `.gitignore` enforcement, secrets scanning, synthetic fixtures for demos, encrypted storage for ingest artifacts.
- **Monitoring & Alerting:** Queue size alerts, anomaly detection on rule changes, checksum attestations for audit log chains, optional SIEM integration before production launch.
- **Supply Chain Hardening:** Pin container digests, use Dependabot/Snyk alerts, require signature verification (Cosign) for deployment artifacts.

## 5. Open Security Questions
- Decide on concrete MFA / auth provider for managed deployment.
- Define maximum acceptable blast radius if a reviewer account is compromised (per-workspace vs global).
- Choose tamper-evident log solution (hash chains in Postgres vs external ledger).
- Determine incident response workflow for override abuse or rule poisoning events.

