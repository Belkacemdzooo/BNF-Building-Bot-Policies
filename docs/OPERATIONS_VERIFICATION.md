# BNF Building Bot — Operational Verification Checklist

## Scope and evidence boundary

This repository contains the public legal-information pages for BNF Building Bot. It does **not** contain the WhatsApp bot runtime, Meta webhook implementation, n8n workflows, database schema, or hosting configuration. A published policy page is not proof that the production system implements the described controls.

The public policy currently states that customer phone numbers and conversation data are retained for service operation and follow-up until a valid deletion request is received, subject to narrow legal/security exceptions. Technical backup copies may remain for a limited period under the provider's backup cycle.

## Required runtime controls

### WhatsApp webhook

- Verify Meta's webhook challenge before accepting the endpoint as configured.
- Verify `X-Hub-Signature-256` against the raw request body using HMAC-SHA256 and the configured Meta App Secret.
- Compare signatures in constant time; reject missing or invalid signatures.
- Validate the expected WhatsApp Business Account / phone-number identifiers.
- Use the Meta message ID as an idempotency key so webhook retries do not create duplicate conversations or replies.
- Never place App Secrets, access tokens, verification tokens, or full message bodies in application logs.

### Data handling and access

- Store only fields required for conversation continuity, support, security, and delivery diagnostics.
- Restrict access to customer conversations by authenticated staff role and organization scope.
- Encrypt transport and use the platform's supported encryption-at-rest controls.
- Keep credentials in a secret store or protected environment variables, never in workflow exports, source files, or commits.
- Record which processors actually receive customer data (Meta, hosting, n8n, AI provider, object storage, monitoring). Update the public policy only after the live configuration is verified.

### Retention and deletion

- Do not apply an automatic expiry to customer phone numbers or conversation records while the agreed retention policy remains in force.
- Accept deletion requests through the published contact route and verify control of the WhatsApp number using a proportionate process. Never request passwords or one-time verification codes by email or chat.
- After verification, delete or irreversibly disassociate the customer's data from every system under our control: primary database, attachments/object storage, queues, caches, n8n execution data, analytics, search indexes, and application logs where applicable.
- Check processor-side retention and deletion capabilities; record any processor-specific limitation.
- Document the backup rotation period. Do not promise immediate removal from immutable backups; ensure backup copies expire through the documented cycle and cannot be restored into normal service without reapplying deletion records.
- Keep a minimal, non-sensitive audit record of the request, verification outcome, completion time, and any lawful exception. Do not retain the conversation body in the audit record.

## Safe verification procedure

- Use synthetic phone numbers, synthetic messages, and isolated test accounts only.
- Test valid and invalid webhook signatures, replay/idempotency behavior, attachment handling, authorization boundaries, and deletion propagation in a non-production environment.
- Test deletion with seeded synthetic records across every store and assert that no customer record remains queryable after completion (excluding documented backup-retention windows).
- Do not send test WhatsApp messages to real customers.
- Do not execute a production deletion, change account permissions, or change billing as part of a routine test.

## Release evidence checklist

Before a release is described as production-ready, attach evidence for each item:

- [ ] Meta webhook challenge and signature verification tests pass.
- [ ] OAuth/token storage and refresh are verified without exposing secret values.
- [ ] Duplicate webhook delivery is idempotent.
- [ ] Role and tenant authorization tests pass.
- [ ] Synthetic deletion test covers every configured data store and processor.
- [ ] Backup retention and deletion replay behavior are documented and tested.
- [ ] Public privacy and deletion pages match the actual deployed processors and retention settings.
- [ ] No real customer message was sent during testing.
- [ ] Deployment has a rollback plan and post-deploy health check.

## Current verification status

As of 2026-11-23, the public GitHub Pages legal site is reachable and its privacy, terms, and data-deletion pages are readable. The separate bot runtime, Meta app configuration, n8n workflow, production database, and deletion execution path have not been verified in this repository. Do not treat this checklist or the published pages as evidence that the runtime controls are implemented.
