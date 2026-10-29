# Architecture decisions

Decisions recorded during the initial project audit on 2026-10-28.

## AD-001: Preserve the original static website as the active public UI

- **Decision:** Keep the existing HTML/CSS/JavaScript website as the default public frontend while dynamic content is added incrementally.
- **Context:** The original website contains 24 HTML pages with existing visual design, navigation, animation, and interactions. The Flutter app is a separate, incomplete prototype and has limited route/content coverage.
- **Tradeoff:** Content is not yet editable through Django on the active static pages. The safe migration path is to connect existing markup to the API a page/section at a time and retain static fallback behavior.

## AD-002: Django is the shared content authority

- **Decision:** Keep site content and public API in one Django application and one database for every frontend client.
- **Context:** Django models cover pages/sections, projects, services, insights, settings, testimonials, FAQs, and contact inquiries. The Flutter client already reads some shared API resources.
- **Tradeoff:** Client-specific presentation belongs in the frontend or a lightweight adapter; do not copy content databases per client.

## AD-003: Use PostgreSQL in the Docker deployment; retain SQLite for local convenience

- **Decision:** Docker Compose uses PostgreSQL with a named persistent volume; Django settings retain SQLite when `DB_ENGINE` is not `postgresql`.
- **Context:** This supports a simple local setup and a shared relational database in the containerized stack.
- **Tradeoff:** Deployment configuration and environment secrets must be explicit. The checked-in SQLite file is not the Docker database source of truth.

## AD-004: Nginx remains the reverse proxy; no separate API gateway

- **Decision:** Continue using the Docker Nginx service to serve the original site and proxy API, admin, and Django static paths.
- **Context:** The project is a single Django backend and one public site. There is no service mesh or multi-service routing need.
- **Tradeoff:** Central gateway features remain limited to the current reverse proxy and application middleware; add policy controls only when an actual need exists.

## AD-005: Django admin is the current content write surface

- **Decision:** Keep create/update/delete operations for site content in the authenticated Django admin; expose only published content through public GET endpoints.
- **Context:** This provides an editable content source without rebuilding the original site or exposing anonymous write APIs.
- **Tradeoff:** The static site must be integrated with read endpoints to reflect edits. Public contact inquiry creation is a separate anonymous operation and needs abuse controls before production use.

## AD-006: Do not version or paginate the initial API without a client need

- **Decision:** Keep current unversioned endpoints and simple response shapes compatible. Reassess pagination as content grows and versioning before external API commitments or breaking changes.
- **Context:** The API is project-local, small in scope, and has no current external consumers.
- **Tradeoff:** Collection sizes are presently unbounded; pagination becomes a priority if content volume or measured response size warrants it.

## AD-007: Manage homepage cards and named section visibility through Django admin

- **Decision:** Use the existing `Service` content resource for homepage cards and a small visibility model for preconfigured homepage sections. Editors upload card images through authenticated Django admin; Nginx serves those files from a persistent media volume.
- **Context:** The homepage slider was hard-coded in HTML, while the Django API/admin and contact inquiry log already existed. Nontechnical editors need clear title/text/image/publish/order fields and simple show/hide controls.
- **Tradeoff:** The homepage cards, hero/intro/latest-work copy and images, named sections, logo, and hero strips are editable now. API failure keeps the original static homepage visible.

## AD-008: Manage the homepage hero strips as a bounded shared resource

- **Decision:** Keep the existing 11 hero strips and their visual layout, but make each strip independently flippable and expose its optional reverse-side team photo, alt text, and visibility through Django admin and `GET /api/hero-panels/`.
- **Context:** The studio wants the black hero strips to flip to a white reverse side on hover/tap and later show team portraits, editable by nontechnical staff.
- **Tradeoff:** The public response is bounded to the 11 fixed slots; empty image fields deliberately render a plain white reverse side. If the hero layout changes its strip count, update the slot choices, seed migration, admin limit, and frontend together.

## AD-009: Keep project inquiries in the existing Django contact resource

- **Decision:** Expand the existing contact page and `ContactInquiry` record to capture company/brand, project type, budget range, and project details. Keep the page in the original static HTML/CSS/JavaScript, preserve the visual system, and send submissions to the shared Django endpoint for review in authenticated admin.
- **Context:** The studio needs a usable creative brief form while preserving the existing website UI and keeping inquiry records in one database. The reference uses a high-contrast condensed heading, ruled form fields, and a separate contact information column.
- **Tradeoff:** The project metadata fields are optional at the API level to keep the existing Flutter `name`/`email`/`message` contract compatible, while the website form requires the intended brief fields. The anonymous endpoint still needs deployment-specific rate limiting and a CSRF review before production exposure.

## AD-010: Track and notify the team about new inquiries

- **Decision:** Add lead status, internal notes, follow-up date, and SMTP-accepted indicator to contact inquiries in Django Admin. Send a plain-text email to an environment-configured team inbox when SMTP host, account credentials, and recipient are configured.
- **Context:** The studio wants the team to notice new leads quickly and manage their follow-up without adding a separate CRM. Submission persistence remains the source of truth if SMTP is unavailable.
- **Tradeoff:** SMTP secrets must be configured privately in local `.env` or deployment secrets. Email is synchronous and best-effort; failures are logged without making a successful inquiry submission appear failed.

## AD-011: Preserve static page markup while CMS fields progressively override content

- **Decision:** Keep the original About, Work, project detail, and insight article HTML/CSS/animation as the UI baseline. Django admin edits approved text and image fields; public pages replace only those values when published CMS data exists.
- **Context:** These pages use carefully styled, interactive page-specific markup. Replacing complete pages with generic CMS rendering risks breaking layout, motion, and legacy routes.
- **Tradeoff:** New page sections and designs still need deliberate frontend integration. Empty/unavailable CMS fields leave static content in place. Uploaded images are public and stored on the existing persistent media volume.
