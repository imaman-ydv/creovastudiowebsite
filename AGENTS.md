# Repository guidance

- Read `docs/architecture/API_DESIGN_RULES.md`, `API_DESIGN_ROADMAP.md`, `API_INVENTORY.md`, `ARCHITECTURE_DECISIONS.md`, and `FUTURE_API_IMPROVEMENTS.md` before changing backend APIs, content models, or frontend data integration.
- Keep the original static website as the public UI unless the user explicitly requests a UI migration. Preserve its routes, styling, assets, animation, and interactions when adding dynamic content.
- Django is the authoritative content backend. All frontend clients must use the same API and database; do not create client-specific copies of business content.
- Reevaluate the eight API patterns in `API_DESIGN_RULES.md` for each backend/data feature. Apply only patterns justified by current requirements, and update the roadmap, inventory, and decision log when the architecture changes.
- Never silently break an existing endpoint or content contract. Add compatibility notes and migration steps for breaking changes.
- Keep secrets out of source control and client builds. Public API views must expose only published content and validate all input.
- Before security-sensitive changes, read `docs/security/SECURITY_ARCHITECTURE.md`, `SECURITY_ROADMAP.md`, `REVERSE_ENGINEERING_PROTECTION.md`, `SECURITY_TESTING.md`, and `SECURITY_DECISIONS.md`. Reevaluate the documented risks and update these records when controls or architecture change.
- Treat Flutter Web, JavaScript, and static assets as inspectable by users. Do not put secrets or authorization decisions in clients; enforce access on Django.
