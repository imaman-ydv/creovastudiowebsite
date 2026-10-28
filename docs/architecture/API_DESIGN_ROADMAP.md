# API design roadmap

Snapshot from repository audit on 2026-10-28. Statuses describe the current project and its next likely trigger, not an assertion that deferred work is already implemented.

| Pattern | Status | Current evidence | Decision / trigger |
|---|---|---|---|
| Resource-oriented design | IMPROVE EXISTING | Django uses named resources for pages, projects, insights, services, settings, testimonials, FAQs, homepage section visibility, hero branding, and hero strips. Content writes are through Django admin. Contact creation is `POST /api/contact/`. | Keep the resource convention. The homepage now reads cards, section visibility, branding, and bounded strip content from shared resources; connect remaining static page content incrementally. |
| Pagination | DEFER FOR FUTURE | Collection GET endpoints return every published row in one response; there is no pagination contract. | Add deterministic, bounded pagination when content volume or payload size affects latency, memory, or page loading. Pick a strategy based on the consumer. |
| Filtering and field selection | DEFER FOR FUTURE | No list query parameters, search, ordering controls, or field selection exist. ORM querysets use model defaults. | Add allowlisted filters/search/sort when a real listing UI requires them. Add field selection only if measured payload needs justify it. |
| Idempotency | DEFER FOR FUTURE | Contact creation inserts one inquiry per request and has no idempotency key. There are no payment/order/job operations. | First disable repeat submission in the UI. Add atomic request idempotency if retries/double-submits must be guaranteed not to create duplicate inquiries. |
| BFF | NOT APPLICABLE NOW | Original static HTML is the active public site; Flutter is a prototype. Both can share the Django API and PostgreSQL database. | Reassess only if a client needs a materially different aggregate/response contract. Keep one authoritative content database. |
| API gateway | NOT APPLICABLE NOW | Django is a monolith. Docker Nginx serves the static site and reverse-proxies API/admin/static paths. | Continue with Nginx. Reassess a dedicated gateway only if multiple backend services or centralized policy needs arise. |
| Asynchronous APIs | NOT APPLICABLE NOW | Current endpoints are short content reads and contact insertion. No queue or long-running job exists. | Reassess for bulk imports, image processing, notifications, or large reports; choose queue infrastructure only for an actual workload. |
| Versioning and evolution | DEFER FOR FUTURE | Endpoints are unversioned under `/api/`; API is currently project-local with a prototype client. | Preserve existing contracts now. Set an external compatibility/version policy before third-party use; add a version for a necessary breaking change. |

## Immediate priorities

1. Keep original static routes and content as the live UI while dynamic integrations are introduced incrementally.
2. The static contact form is wired to the inquiry resource with server-side body/content-type/field validation, a honeypot, and repeat-submit prevention. Before production, choose and configure deployment-appropriate rate limiting and reassess CSRF for both same-origin HTML and Flutter callers. Decide whether request idempotency is needed based on retry behavior.
3. Define a consistent API error/response contract and secure production settings before exposing the API beyond the local Docker stack.
4. Add endpoint tests when implementation work changes API behavior; cover published-content filtering, validation/status codes, permissions, and regression compatibility.

## Deferred triggers

- Pagination: project/article collections become large, responses slow or grow too large, or a client needs page-by-page loading.
- Filtering/search: the editorial UI adds category, text search, or sort controls.
- Idempotency: network retries or repeat submits must be guaranteed to produce one inquiry.
- BFF/gateway: a second supported client or backend service reveals a specific aggregation, routing, or policy gap that the existing shared API and Nginx cannot address simply.
- Async jobs: an operation no longer fits a normal request/response time budget.
- Versioning: an external client needs a breaking API contract change.
- CMS coverage: connect other static pages and images to content models when the matching editor fields and fallback behavior are ready.
