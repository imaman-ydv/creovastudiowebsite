# Security testing procedures

These are planned repeatable checks based on the current Django, Flutter Web, and Docker stack. They have not been run as part of the documentation-only audit. No automated security scanner configuration was found.

## Django checks

Run from `backend/` with the project environment and test database configured:

```sh
python manage.py check
python manage.py check --deploy
python manage.py test
```

For future endpoint changes, add tests covering:

- Anonymous reads return only published records and only public fields.
- Unpublished pages/sections/items are hidden and unknown slugs return 404.
- Public settings output contains only explicitly allowed keys.
- Contact rejects malformed JSON, wrong content type, missing fields, invalid email, and excessive body/field size; valid input preserves the documented `201` response.
- Only authorized staff can upload homepage images; malformed files, unsupported extensions, and images over 8 MB are rejected, and accepted images are served as public content from `/media/`.
- Contact rate controls behave correctly behind the production proxy and do not throttle unrelated users unexpectedly.
- Admin requests require authentication and content writes require the appropriate Django permissions.
- Future user-owned data enforces object-level authorization on the server, including cross-user/tenant denial.

## Browser and Flutter Web checks

- Verify all public pages still render and navigate after security header/CSP changes.
- Confirm current menu, page transitions, GSAP/Barba interactions, images, and analytics behavior while reviewing external script sources.
- Inspect production responses for HTTPS, secure cookies where applicable, CSP, frame restrictions, MIME sniffing, and referrer policy.
- Verify Flutter Web sends only public API configuration and no secret/token in compiled assets or browser storage.
- Test legitimate contact submission, duplicate clicks, error responses, and CORS from the intended deployed origins.

## Container and dependency checks

- Confirm the public host exposes only the intended Nginx port; database and Gunicorn remain on internal networks.
- Confirm production startup rejects `DEBUG=True`, placeholder Django secret, placeholder database password, wildcard hosts/origins, and missing HTTPS policy.
- Inspect runtime UID, writable paths, database grants, image provenance, and health checks.
- Confirm the media volume survives container recreation, is read-only to Nginx, and is included in the documented backup/restore workflow.
- Scan Python dependencies, Flutter dependencies, and built container images; review findings before upgrades.
- Validate that `.env`, database files, backups, signing material, and debug symbols are not committed or published.
- Before production data is trusted, restore a backup into an isolated environment and verify content/inquiry recovery.

## Reporting

Record tool name/version, command, date, environment, findings, false-positive rationale, and remediation status. Never report a scan or check as successful unless it actually ran and its output was reviewed.
