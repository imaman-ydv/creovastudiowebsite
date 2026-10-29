# API inventory

Snapshot from `backend/content/urls.py`, views, models, and Flutter API client on 2026-10-28.

Base path: `/api/` (unversioned). Django is mounted behind Nginx in Docker. Public JSON responses use Django `JsonResponse`; collection payloads currently use `{"results": [...]}` except settings, which returns a key/value object. No standard pagination envelope is implemented.

| Endpoint | Method | Access | Current response / behavior |
|---|---|---|---|
| `/api/pages/` | GET | Anonymous | `{"results": [...]}` for published pages; each page embeds its published sections. |
| `/api/pages/{slug}/` | GET | Anonymous | One published page with metadata and published sections; missing/unpublished page returns 404. |
| `/api/projects/` | GET | Anonymous | `{"results": [...]}` for published projects; includes id, title, slug, client, year, category, summary, effective cover image URL, image alt text, website URL, and featured flag. |
| `/api/projects/{slug}/` | GET | Anonymous | One published project with its editable text, effective cover image, alt text, website URL, and ordered gallery. Missing/unpublished slugs return 404. |
| `/api/insights/` | GET | Anonymous | `{"results": [...]}` for published insights; includes title, slug, excerpt, effective cover image URL, alt text, body, and optional publication time. |
| `/api/insights/{slug}/` | GET | Anonymous | One published article with its editable title, excerpt, body, cover image and ordered gallery. Missing/unpublished slugs return 404. |
| `/api/services/` | GET | Anonymous | `{"results": [...]}` for published services. |
| `/api/sections/` | GET | Anonymous | `{"results": [...]}` containing the registered homepage section keys, labels, and visibility state. |
| `/api/branding/` | GET | Anonymous | Homepage hero logo URL, accessibility description, and size percentage (86% default); uses the bundled logo when no upload exists. |
| `/api/hero-panels/` | GET | Anonymous | `{"results": [...]}` for the homepage's 11 ordered hero strips; each includes slot, visibility, optional uploaded team photo URL, and alt text. |
| `/api/settings/` | GET | Anonymous | Object mapping setting keys to values; currently returns all settings. Review which settings are safe for public output before adding private settings. |
| `/api/testimonials/` | GET | Anonymous | `{"results": [...]}` for published testimonials. |
| `/api/faqs/` | GET | Anonymous | `{"results": [...]}` for published FAQ items. |
| `/api/contact/` | POST | Anonymous | Accepts JSON `name`, `email`, `details` (or legacy `message`), `company_brand`, `project_type`, and `budget_range`; validates content type, a 12 KB body limit, required contact/details fields, lengths, and email; creates a `ContactInquiry`; returns `201 {"ok": true, "id": ...}`. `company_brand`, `project_type`, and `budget_range` are optional for backwards compatibility with Flutter clients. Invalid requests return `400`, `413`, or `415`. Honeypot submissions return a successful empty result without storage. If SMTP credentials and a recipient are configured, a plain-text notification is sent to the configured team inbox with visitor email as `Reply-To`; SMTP acceptance is recorded on the inquiry, and delivery failure does not undo the saved inquiry. View remains CSRF-exempt; no IP rate limit or idempotency key is implemented. |
| `/admin/` | Django admin methods | Authenticated staff/superuser according to Django admin permissions | CRUD for content models and inquiries. This is a server-rendered admin interface, not a public content API. |

## Contract and implementation notes

- All list endpoints are unpaginated. Existing ORM `Meta.ordering` provides default ordering, but no API-level ordering contract is documented.
- No public API endpoint currently accepts filters, search, sort, or field selection.
- Content API is read-only to anonymous callers; content changes are made using Django admin.
- `/api/services/` includes the public card image URL (uploaded image first, existing static image fallback otherwise), image description, link label and destination, and optional `read_more_content` shown in the homepage card dialog. Uploads happen only through authenticated Django admin, not through a public API.
- `/api/branding/` exposes the current homepage hero logo. Authorized staff replace the image, edit its accessibility description, and set its display size in the **Homepage hero logo** Django admin section; resizing keeps it centered, while scroll parallax moves it down only within the available edge gap.
- `/api/hero-panels/` exposes the bounded 11-strip hero configuration. Staff upload an optional photo, edit its description, or hide a strip in the **Homepage hero logo** admin page; missing photos leave a white reverse face, while the static strip layout remains the fallback if the API is unavailable.
- The original homepage fetches `/api/pages/home/` for its hero heading, intro copy/images, latest-work feature, client showcase heading/image, and services heading/intro. API failure leaves the original static values in place.
- Homepage cards are managed in **Homepage cards** in Django admin, with title, main/supporting text, read-more copy, image, accessibility description, visibility, sort position, and optional link. The card endpoint returns only published rows; `home-cms.js` retains the source static cards if the API is unavailable.
- Homepage hero logo and its 11 interactive strips remain editable under **Homepage hero logo**; the named homepage sections can be shown/hidden under **Website sections**. All these settings continue to share the same CMS database and persistent image volume.
- About has seeded `SitePage` / `PageSection` records for its main heading, intro, approach, principles, section images, and help intro. The existing static page remains the fallback; section images can be uploaded from admin.
- Work's three active cards are seeded as published projects; work card copy, year, and image updates are read from `/api/projects/`. Project detail pages (the eight `projects/*.html` files plus Krishadha, EGM MART, and MENMI) use the slug detail endpoint; uploaded project story text and gallery images replace the static story only when a story is supplied.
- Insight article pages use `/api/insights/{slug}/`; editors can update title, excerpt, cover, long-form body, and ordered inline images. Empty article bodies preserve the original static article markup.
- Project, Insight, and PageSection admin uploads accept JPG, PNG, or WebP up to 8 MB. Public endpoints return only published parent content; uploads remain staff-only and are served from the persistent `/media/` volume.
- Homepage section visibility is limited to preconfigured named sections. Editors choose a visible checkbox and do not enter selectors or code.
- The Django admin accepts service card images in JPG, PNG, or WebP up to 8 MB. Nginx serves uploads from a persistent Docker volume at `/media/`.
- Flutter `SiteApi` currently consumes projects, insights, and contact submission only. The original static contact page now submits project briefs to the same API; prior Flutter `name`/`email`/`message` submissions remain accepted.
- Django Admin tracks inquiries as New, In progress, Won, or Lost, with private internal notes and a follow-up date. SMTP delivery is configured only through environment variables and is skipped until host, user, password, and recipient are set.
- The project contains 24 original website HTML files across root, `projects/`, and `insights/`, plus the Flutter `web/index.html`; routes and markup are file-based, not Django-managed routes.
- No OpenAPI schema, API version prefix, endpoint-specific permission classes, or dedicated API test cases were found during this audit. `backend/content/tests.py` is only the generated empty test skeleton.
