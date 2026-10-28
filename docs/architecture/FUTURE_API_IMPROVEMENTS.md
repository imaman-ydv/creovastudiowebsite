# Future API improvements

This is a prioritized backlog, not a statement that the items are implemented.

## Before production API exposure

- Replace local fallback secrets and database credentials with deployment-managed secrets; set `DEBUG=False`, exact allowed hosts, trusted origins, and CORS origins.
- Review the public `GET /api/settings/` response so only intended public settings can be returned.
- The contact endpoint now enforces JSON content type, a 12 KB request-body limit, server-side field/email validation, and a honeypot; the static form prevents repeat clicks while a request is pending. Choose and configure deployment-appropriate rate limiting and reassess CSRF before production exposure.
- Decide whether contact submission needs an idempotency key based on retry semantics; if needed, implement it atomically and test conflicting/concurrent reuse.
- Add API contract tests for published-only visibility, request validation, response status/body, admin authorization, and proxy-compatible URLs.

## When content volume or editor needs grow

- Add bounded pagination to project and insight collection endpoints after confirming the client behavior and stable ordering.
- Add allowlisted category/search/sort query parameters only for real UI controls.
- Consider replacing free-form section JSON with validated typed fields/schemas if the admin authoring surface becomes hard to use or frontend data errors become common.
- Add admin media fields as more static page media is connected; homepage card and hero-strip photos use Django admin and the persistent Docker media volume.
- Define a generic form schema/submission workflow if the site adds forms beyond the current contact project brief (`name`, `email`, company/brand, project type, budget range, and details).

## Before adding clients or integrations

- Keep Flutter and static site on the same Django API/database; add only thin client adapters if response needs differ.
- Publish a versioning/deprecation policy before third parties depend on the API.
- Add a dedicated gateway or BFF only after documenting a concrete gap that Nginx and the shared API cannot handle simply.

## When operations become long-running

- Evaluate an asynchronous job queue only for real bulk imports, image processing, notifications, or large reports. Define status, retries, backoff, failure visibility, duplicate execution handling, and cancellation requirements first.

## UX regression coverage for gradual migration

- For every page connected to dynamic content, compare its desktop/mobile layout and key interactions against the original static page.
- Keep a content-empty or API-error fallback so a temporary backend issue does not blank the public site.
- Add browser/API integration coverage alongside the existing visual behavior; no such API test suite was found in the initial audit.
