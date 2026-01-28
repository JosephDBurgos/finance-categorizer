# Project Brief

## Problem Statement
Personal financial data is scattered across multiple banks, card providers, and payroll systems. Raw CSV exports make it difficult to see where money goes, why balances change, and whether spending aligns with goals. This project will provide an automated, multi-user workflow that normalizes transactions, enforces strong tenant isolation, and assigns consistent categories so insights are repeatable and shareable without compromising security.

## Target User
- **Primary (now):** Myself plus a small circle of trusted collaborators who need a secure shared workspace for budgeting experiments and audit trails.
- **Secondary (later):** Small households or clubs that require invitation-only access, per-user accountability, and transparent categorization logic.

## Explicit Non-Goals
- No consumer mobile app or push notifications during v1.
- No third-party data aggregation services that store user credentials server-side.
- No opaque ML categorization until rule coverage and evaluation metrics are solid.

## Success Criteria
- Import 12 months of transactions from at least two institutions into the canonical schema with zero data loss.
- Automatically categorize ≥80% of new transactions with human-auditable reasoning.
- Produce a daily diff report highlighting uncategorized or low-confidence items for each workspace.
- Manual edits persist across re-imports via idempotent reconciliation.
- Support at least five concurrent users with role-scoped permissions, MFA-backed sign-in, and isolated data stores per workspace.


## Key Constraints
- **Privacy & Security:** Default to encrypted at-rest storage, per-tenant encryption keys, and no third-party APIs for storage or enrichment without opt-in agreements.
- **Correctness > Coverage:** A transaction stays uncategorized rather than risk misclassification.
- **Explainability:** Every automatic decision cites the rule, user, data source, and timestamp.
- **Portability:** Avoid vendor-specific formats; all artifacts should survive repository cloning without secrets, while user credentials remain externalized.
