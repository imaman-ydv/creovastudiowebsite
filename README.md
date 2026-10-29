# Creova Studio

The public website is still the original HTML/CSS/JavaScript site in this folder. It remains the default so its pages, visual design, animations, and navigation stay available while dynamic editing is added.

- `backend/` — Django admin and JSON API for editable site content.
- `frontend/` — Flutter prototype; it is not the public website yet.

## View the existing website

Start the default Docker stack from this folder, then open `http://localhost:8080`:

```sh
cp .env.example .env
docker compose up --build
```

The default stack serves the original HTML/CSS/JavaScript site through Nginx, runs Django and PostgreSQL in separate containers, and routes `/api/`, `/admin/`, and `/static/` to Django. Create the first admin login with `docker compose exec backend python manage.py createsuperuser`, then open `http://localhost:8080/admin/`.

## Manage homepage content, cards, and sections

In Django admin, use **Homepage cards** to edit the homepage service cards. Team members can change the title and text, upload a JPG/PNG/WebP image, set its accessibility description and link, add optional **More to read** content for the card popup, turn a card on/off, and change its position. Uploaded images are stored in the persistent `uploaded_media` Docker volume and served by Nginx.

Use **Pages → Homepage** to edit the hero headline, introduction copy and images, Latest Work feature, client showcase heading/image, and services heading/intro. Use **Pages → About** for the About page copy and images. The original HTML, layout, and animations remain the fallback if CMS content cannot load.

Use **Homepage hero logo** to replace the large centered logo shown in the homepage hero, update its accessibility description, and adjust its size from 30% to 100% (86% by default, leaving a clear gap around it). The logo stays centered when resized; on scroll it scales and moves down only within the remaining edge gap, with a continuous breathing effect. The uploaded logo is stored in the same persistent media volume; the original `images/Logo.avif` remains the fallback.

On the same **Homepage hero logo** editor, use **Homepage hero strips** to manage the 11 vertical hero panels. Hover or focus a strip to flip it; tap/click or press Enter/Space to keep it flipped. Upload an optional team photo and write its description for each strip, or hide that strip. Empty photo slots flip to a plain white back.

Use **Website sections** to show or hide the homepage hero, introduction, latest work, client showcase, and services area. The section list is preconfigured so editors do not need to enter CSS selectors or code.

Use **Form submissions** to review contact inquiries received by the contact page through `POST /api/contact/`. Set each inquiry to New, In progress, Won, or Lost; add private team notes and a follow-up date; and mark it reviewed. The list shows whether the SMTP server accepted the notification. New inquiries send a plain-text email to the configured contact notification address once SMTP is configured. The endpoint also keeps accepting the older Flutter `name`/`email`/`message` request format.

To receive email notifications locally, set the SMTP variables in the root `.env` file before starting Docker. The example is prefilled for Gmail at `studiocreova@gmail.com`; create a Google App Password for SMTP and put it in `EMAIL_HOST_PASSWORD`. Keep that password private and out of Git. Set `CONTACT_NOTIFICATION_EMAIL` to the inbox the team should monitor. Without configured SMTP credentials, inquiries still save in Admin and no email is sent.

For team access, a superuser can add a staff user under **Authentication and Authorization → Users** and grant only the required content permissions (or assign a permission group). Do not share the superuser login with the team.

Use **Projects** to edit work cards and project detail metadata, cover photos, story text, and gallery images. Use **Insights** to edit article titles, excerpts, cover photos, story text, and gallery images. Existing static detail pages remain visible when optional long-form CMS text is left empty.

To stop the stack, press `Ctrl+C`. For Vercel, the project root should be this folder (the one containing `index.html`). The `getdesign add vercel` command does not configure deployment.

## Render testing deployment

`render.yaml` defines a temporary Render Blueprint with the site, Django backend, portfolio, and a free PostgreSQL database. In Render, create a **Blueprint** from this repository and select the branch containing this config. During setup, enter a strong value for `DJANGO_SUPERUSER_PASSWORD`; Render stores it as a secret, and the backend creates `creova_admin` once. The password is never stored in this repository. Admin is available at `/admin/` on the site URL, and the portfolio is available at `/portfolio/`.

This is for testing only: free web services can sleep when idle, uploaded images are ephemeral, and the free database expires after 30 days. Render Free blocks SMTP ports used by the current notification setup, so inquiry records remain available in Admin but email notifications will not deliver there. Export content and images before removing the test deployment.

The incomplete Flutter prototype is an optional preview only. To run it in Docker, use `docker compose --profile flutter-preview up --build` and open `http://localhost:8081`.

## Local development

### Django API

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The admin is at `/admin/`. The public API starts at `/api/`:

- `GET /api/pages/` and `GET /api/pages/<slug>/`
- `GET /api/projects/`
- `GET /api/insights/`
- `GET /api/hero-panels/`
- `GET /api/services/`, `/api/settings/`, `/api/testimonials/`, `/api/faqs/`
- `POST /api/contact/` with JSON fields `name`, `email`, `company_brand`, `project_type`, `budget_range`, and `details` (or legacy `message`)

The admin lets you edit page sections, projects, services, insights, site settings, testimonials, FAQs, contact inquiries, the homepage hero logo, and each hero strip. Page sections have a section type plus editable text, image/link fields, and a JSON data field for page-specific content.

Use `backend/.env.example` as a reference and export those values in your shell or enter them in deployment settings. Django does not load that file automatically. Its values are for local development; production must use a private secret key, PostgreSQL credentials, allowed hostnames, frontend CORS origin, and SMTP secrets from deployment configuration.

### Flutter Web

```sh
cd frontend
flutter pub get
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8000/api
```

The Flutter prototype is separate and incomplete. Do not use it as the public website while it is being evaluated.

## Dynamic content status

The original static pages remain the public site. Homepage service cards, named section visibility, hero logo, and the 11 flip-enabled hero strips are connected to Django while retaining the existing HTML/CSS layout. Django admin also manages projects, insights, pages/sections, site settings, testimonials, FAQs, and form submissions, but those other content types are not yet connected to the original static pages. Connect them incrementally while keeping the current markup, styling, and interactions.
