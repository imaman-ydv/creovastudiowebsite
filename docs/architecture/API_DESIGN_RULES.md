# API design rules

These rules apply to the Creova Studio Django API and any future frontend integration. The production website currently remains the original static HTML/CSS/JavaScript site; architectural changes must preserve its existing UI and behavior unless the user requests otherwise.

## 1. Resource-oriented design

- Use plural, resource-based paths and standard HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`). Use action endpoints only when an operation is not naturally a resource.
- Keep response fields, status codes, validation errors, and trailing-slash conventions consistent.
- Public content endpoints expose published content only. Django admin is the authenticated write interface for content.
- Keep existing paths and response contracts compatible. Document migrations before breaking a client.

## 2. Pagination

- Evaluate collection growth and payload size whenever adding or changing a list endpoint.
- If a collection can grow materially, choose page-number pagination for editorial browsing or cursor pagination for larger/changing feeds. Include deterministic ordering with a unique tie-breaker and enforce a maximum page size.
- Keep small, bounded collections unpaginated when paging adds no meaningful value. If pagination is introduced, update every consumer to follow pages.

## 3. Filtering, searching, sorting, and field selection

- Add only filters that correspond to real UI needs; allowlist filter and ordering fields and validate values.
- Optimize ORM access for actual response shapes; avoid exposing unrestricted model fields.
- Do not add arbitrary field selection until there is a concrete client or payload need. Any selectable field must be allowlisted and public-safe.

## 4. Idempotency

- Identify create operations that can be retried and produce duplicate side effects. For a public contact form, first prevent repeated UI submissions and assess observed duplicate risk; add scoped, atomic idempotency keys only if retry-safe behavior is required.
- If idempotency keys are added, bind them to operation and caller scope, compare request payloads, handle concurrent use atomically, define expiry, and reject key reuse with a conflicting payload.
- Do not mistake idempotency keys for business-level duplicate detection.

## 5. Backend for frontend (BFF)

- Prefer the shared Django API while static and Flutter clients need the same content. A client-specific response adapter is acceptable if it calls the same backend resources.
- Never create separate authoritative content stores for each frontend. Keep identifiers, authorization, writes, and cache behavior consistent.
- Add a BFF only after a concrete client-specific need cannot be handled cleanly in the shared API.

## 6. API gateway

- The current Docker Nginx container is the public reverse proxy for the website and routes `/api/`, `/admin/`, and `/static/` to Django. Keep using it for simple routing and TLS/deployment integration.
- Do not introduce a separate gateway or microservices for this Django monolith. Reassess only if central policies, multiple services, or scale make the added layer worthwhile.

## 7. Asynchronous APIs

- Keep ordinary content reads and contact submissions synchronous while they are short and bounded.
- Reassess background jobs for bulk import, image processing, large reports, notifications, or other work that exceeds a normal request budget.
- Add queue infrastructure only with a concrete job requirement, including status, retries/backoff, failure visibility, duplicate execution protection, and transaction safety.

## 8. Versioning and evolution

- Keep changes backward-compatible while the API is internal to this project and its clients are updated together.
- Before external consumers rely on the API, choose a documented versioning policy. Introduce a new version only for a breaking contract change; document deprecation dates and migration steps.
- Expand response fields and optional query parameters compatibly. Do not silently rename or remove fields.

## Security baseline

- Treat every request as untrusted. Validate inputs server-side and expose only public/published data from anonymous endpoints.
- Keep content writes behind Django admin authentication and permissions. Never trust the frontend to enforce authorization.
- Review CSRF/CORS, host/origin policy, abuse controls, sensitive output, database integrity, and safe errors whenever an endpoint is added or changed.
- Keep secrets in environment/deployment configuration, not source or Flutter compile-time values.
