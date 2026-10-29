# Security architecture and initial audit

Audit snapshot: 2026-10-28. This is a code/configuration review of the local repository. No production domain, cloud environment, credentials, or deployment was supplied, so the review does not assert the state of any live deployment. No secret-scanning or dependency-vulnerability scanner was run.

## A. Project security overview

- **Public UI:** 24 original static HTML pages, CSS, JavaScript, images, and project/article content, served by Nginx in Docker. Browser-delivered code and content are public and inspectable. Pages load third-party scripts/assets including Webflow, Google Tag Manager, GSAP, Barba, Lenis, and Slater.
- **API/admin:** Django 6.x application. Anonymous GET views return public content; the contact view accepts anonymous submissions. Django admin provides authenticated content editing and inquiry viewing.
- **Data:** Content, inquiries, and admin identities are stored in Django's relational database. Docker Compose uses PostgreSQL with a named volume; local settings fall back to SQLite. Contact inquiries contain names, email addresses, messages, project details, and lead notes. Optional SMTP notifications include inquiry PII and use environment-provided credentials with TLS; service card images are uploaded only through authenticated Django admin and stored in a persistent Docker volume.
- **Other client:** Flutter Web is an optional prototype. It requests project/insight data and submits contact messages. No Android or iOS targets were found in the frontend tree. The web build and its API requests are inspectable.
- **Edge/deployment:** Docker Compose exposes Nginx on port 8080 and keeps Django/PostgreSQL on the internal Compose network. Nginx routes `/api/`, `/admin/`, and `/static/`. Nginx itself has no TLS listener or explicit response-security-header policy; production TLS may be handled by an external host, which was not available to inspect. The optional Render Blueprint is for temporary testing only; its free web services have ephemeral filesystems and its database expires after 30 days.
- **Build/dependencies:** Python dependencies use open version ranges in `backend/requirements.txt`; Flutter has a `pubspec.lock`. Docker image tags are not pinned by digest. No CI workflow or automated security scanning configuration was found in the inspected repository files.

## Trust boundaries and assets

| Boundary / asset | Security significance |
|---|---|
| Visitor browser ↔ Nginx/static site | HTML, JavaScript, images, and requests are public. Third-party scripts execute in the page origin and can affect page behavior. |
| Browser/Flutter Web ↔ public API | Client input is untrusted. Public content reads are intended; contact submission is anonymous by design. CORS does not replace API authorization. |
| Editor ↔ `/admin/` | Django authentication and permissions protect content writes and inquiry access. Admin passwords and session cookies are privileged assets. |
| Django ↔ PostgreSQL/SQLite | Contact PII and editable site content require confidentiality, integrity, backups, and controlled access. Compose does not publish the database port to the host. |
| Build/deployment configuration | Django secret key and database credentials must be unique, private, and environment-specific. Current Compose fallbacks are explicitly local placeholders and are unsafe for public deployment. |

## Existing controls verified in code/config

- Django password validators are enabled for password changes/creation through Django flows.
- Django session, authentication, CSRF, clickjacking, and security middleware are configured; `SecurityMiddleware` and `XFrameOptionsMiddleware` are present.
- Content list/detail views filter by `published=True`, except site settings, which return all rows.
- Contact input requires JSON, is limited to 12 KB, checks required fields and maximum lengths, validates email server-side, and quietly discards honeypot submissions. The static form prevents repeated clicks while a request is pending. The body is inserted through Django ORM, not handwritten SQL.
- Django admin protects content write workflows with Django authentication/permissions. Inquiry contents are read-only in the admin form.
- The Render test Blueprint can create an initial admin only when all three `DJANGO_SUPERUSER_*` environment values are set. The password is deployment-only, validated against Django's password validators, never logged, and never changes an existing account's password.
- CORS origins are explicitly listed when `DEBUG=False`; however, `DEBUG=True` enables allow-all CORS in settings.
- Database service is on the private Compose network; only Nginx publishes a host port.
- Homepage card uploads use Django `ImageField`/Pillow validation, an 8 MB application limit, JPG/PNG/WebP extension allowlist, authenticated admin upload, and a media volume mounted read-only in Nginx. SVG/HTML uploads are not accepted. Uploaded media is intentionally public because it is used by published website cards.
- `.env` is ignored by Git and examples contain local placeholders. No actual production secret was verified in these examples.

## B. Vulnerability assessment

Severity is conditional on exposure. No critical exploitable vulnerability was confirmed in this repository-only review.

| Severity | Finding | Affected component / realistic threat |
|---|---|---|
| **High if deployed with defaults** | Compose defaults `DJANGO_DEBUG=true`, a fixed Django secret key, and a known local PostgreSQL password. A public deployment using these fallbacks can expose diagnostic data, weaken signed session/token integrity, and allow database access if the database is reachable. | `docker-compose.yml`, `.env.example`, Django settings. Local-only defaults are acceptable only while the stack remains local. No live deployment was inspected. |
| **Medium** | Public contact submission has no application rate limit or idempotency, and remains CSRF-exempt. The form has a honeypot and repeat-submit prevention, but automated traffic can still create inquiries. | `backend/content/views.py`, `/api/contact/`. Apply deployment-appropriate rate limiting and complete the CSRF review before production. |
| **Medium, conditional on stored values** | `/api/settings/` serializes every `SiteSetting` key/value without a public/private flag or allowlist. An editor could accidentally publish a value intended to remain private. | `backend/content/views.py`, `SiteSetting`. No private setting value was confirmed in data. |
| **Medium before production** | Explicit HTTPS/TLS, secure-cookie/HSTS policy, and Nginx security headers are not configured in the checked-in deployment. An external TLS termination layer may exist but was not supplied. | `docker/nginx.conf`, `backend/config/settings.py`, deployment edge. HTTP is suitable for current local development only. |
| **Medium** | Public static pages load multiple third-party scripts, with no site-wide Content Security Policy; many script tags do not declare Subresource Integrity. A compromised/upstream script can run with the website's browser privileges. | Static HTML pages and third-party CDNs/analytics. A strict CSP may break existing animation/analytics and requires a compatibility inventory/report-only rollout. |
| **Medium before production** | Dependencies use ranges rather than a complete Python lock with hashes; Docker tags can move; no CI dependency/secret scanning was found. This increases unreviewed supply-chain update risk. | `backend/requirements.txt`, Dockerfiles, Flutter lockfile, CI configuration. No vulnerability scan was performed. |
| **Low/Medium operational** | Backend and Nginx container images do not set a non-root runtime user; PostgreSQL app credentials use Compose's initialization user; no backup/restore procedure is documented in repository configuration. | Dockerfiles, Compose volume. Host/container deployment behavior and backup services were not inspected. |
| **Informational / future client risk** | Flutter Web and static JavaScript can be downloaded and reverse engineered. No private API key or privileged credential is needed in these clients; web obfuscation would not provide secrecy. | `frontend/`, static site. Authorization must remain on Django. |
| **Low/Medium operational** | Uploaded site images are public static files and are not malware-scanned. Admin upload access is restricted to Django staff permissions, and upload handling restricts image extensions and size. | `Service.card_image`, page sections, projects, insights, `MEDIA_ROOT`, Nginx `/media/`. Add malware scanning only if upload exposure or business needs justify it. |

## Authentication and authorization

- Django admin is the only current authenticated workflow. No custom end-user, tenant, or object-ownership model was found.
- Public content API endpoints are intentionally anonymous and read-only. They should disclose only published, public fields.
- Contact creation is intentionally anonymous. It must receive abuse controls before public production exposure.
- No login throttling, MFA, admin IP restriction, or application-level audit trail was found. Prioritize admin login protection based on the actual hosting environment and threat model.

## Data protection

- ORM use helps avoid raw SQL injection in the inspected views. Django's ORM and validators do not prevent unsafe frontend rendering; future templates/DOM code must escape content and constrain URL schemes.
- PostgreSQL is not host-published in Compose. Encryption at rest, off-host backups, backup retention, restore drills, and production role separation are not configured here.
- Do not store credentials, tokens, or other secrets as ordinary site settings. Public API serialization needs an explicit public allowlist.
- Contact messages are PII. Define access, retention/deletion, backup, and incident handling policies before production.
- Uploaded card images are public content, not private documents. Back up the persistent media volume alongside the database; keep uploads limited to approved raster formats and do not expose an anonymous upload API.

## C. Immediate security fixes

No runtime code/configuration has been changed in this audit. The first implementation batch should make production misconfiguration fail closed and keep local development convenient:

1. Make production `DEBUG=False` and require a non-placeholder Django secret, unique PostgreSQL credentials, exact allowed hosts, and HTTPS origins. Consider keeping explicit local defaults behind a clearly named development profile, not implicit production fallbacks.
2. Restrict public settings output to an explicit allowlist or add a `public` field with safe default false; add tests that secret-like/private values never appear.
3. Choose deployment-appropriate contact rate limiting and complete the CSRF review; request-size/content-type checks, a honeypot, validation, and browser repeat-submit prevention are now in place. Preserve existing successful response compatibility.
4. Add security headers and TLS policy at the actual production TLS edge. Roll out CSP in report-only mode after inventorying the required current CDN/script sources.

These changes are appropriate before public deployment. If this Docker stack is being used only on a local machine, the first item is a production-readiness blocker rather than evidence of a current remote compromise.

## D. Production readiness

**Not production-ready from repository configuration alone.** The current Docker Compose settings are local development defaults. Before public exposure, verify production secrets/debug/host/origin settings, HTTPS and security headers, anonymous contact abuse controls, public-setting allowlisting, admin protection, dependency/container scanning, and database backup/restore. The actual production edge, data, credentials, and hosting settings remain unverified.
