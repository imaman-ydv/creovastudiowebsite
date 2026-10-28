# Security decisions

Initial decisions recorded 2026-10-28. These preserve current local development and public website behavior while identifying production blockers.

## SD-001: Treat static and Flutter Web clients as untrusted public clients

- **Decision:** Keep secrets and authorization on Django; do not treat browser code, hidden routes, obfuscation, or official-client identity as access control.
- **Reason:** All web assets and requests are inspectable and modifiable.
- **Tradeoff:** Business rules that require secrecy or privileged access must execute in the backend.

## SD-002: Keep current public reads anonymous, with published-only data

- **Decision:** Public website content remains anonymously readable; content edits stay behind Django admin authentication/permissions.
- **Reason:** The product is a public studio website with no user account feature found in the repository.
- **Tradeoff:** Anonymous contact submission needs abuse protection. Every newly exposed field must be checked for public safety.

## SD-003: Keep local Docker defaults local; fail closed in production

- **Decision:** Fixed placeholder secrets, `DEBUG=True`, and local PostgreSQL credentials are for local development only. Production deployment must set explicit secure values and reject placeholders.
- **Reason:** Current Compose values are convenient locally but unsafe if copied into a public deployment.
- **Tradeoff:** Production startup becomes stricter; local development keeps a documented explicit path.

## SD-004: Do not add mobile anti-tamper controls to Flutter Web

- **Decision:** Do not add Android/iOS attestation, root checks, debugger checks, or Dart obfuscation as a secrecy boundary for the current Web target.
- **Reason:** No native mobile target exists; web output is inspectable and obfuscation cannot protect secrets.
- **Tradeoff:** If native clients or high-value client-bound operations are added, reassess native signing/attestation with server-side verification.

## SD-005: Stage CSP and third-party script changes

- **Decision:** Inventory existing script and asset origins, begin CSP in report-only mode, then tighten sources based on observed behavior.
- **Reason:** The static site depends on multiple external animation, Webflow, and analytics scripts. A strict immediate CSP could silently break the UI.
- **Tradeoff:** The site remains exposed to third-party script supply-chain risk until sources are reduced and policy is enforced.

## SD-006: Do not change production data or credentials during audit

- **Decision:** This initial audit only reads source/configuration and writes security documentation. It does not rotate credentials, edit live records, deploy, or alter a database volume.
- **Reason:** Production environment and ownership were not supplied, and the request asks for an audit and plan before major changes.
- **Tradeoff:** Identified controls remain unimplemented until the implementation phase.

## SD-007: Accept homepage image uploads only through Django admin

- **Decision:** Let authenticated staff upload JPG, PNG, or WebP homepage card images up to 8 MB. Validate the decoded image, store it in a persistent media volume, serve it publicly through Nginx, and do not create an anonymous upload endpoint.
- **Reason:** Nontechnical editors need to replace card images without editing files or source code. These images are intended for public website display.
- **Tradeoff:** Media volume backups are required. SVG/HTML uploads and private image workflows are not supported; add malware scanning if the upload risk or business needs change.
