# Reverse-engineering and client integrity

Audit snapshot: 2026-10-28.

## Current clients

- The active website is static HTML, CSS, and JavaScript. All delivered code, URLs, markup, and requests are available to a visitor's browser tools.
- The optional Flutter target is Flutter Web. Its JavaScript/Wasm assets and API traffic are likewise inspectable. The compile-time `API_BASE_URL` is routing information, not a secret.
- No Android/iOS native target, signed mobile release, desktop app, native credential storage, or client integrity attestation was found.

## Decision

**Web reverse-engineering resistance: NOT APPLICABLE as a secrecy control.** Do not obfuscate or encrypt browser code expecting it to hide business logic or credentials. Any real authorization, private integration secret, and privileged operation must stay on the Django server. The backend must treat the static and Flutter clients as modifiable and independently enforce permissions.

**Native mobile hardening: DEFER FOR FUTURE.** If Android/iOS targets are introduced, assess release signing, platform-secure credential storage, supported obfuscation/minification, private symbol handling, and server-verified attestation for high-value operations. Root/jailbreak/debugger signals should remain risk indicators, never the only access gate.

## Practical protections now

- Never compile Django/PostgreSQL credentials, private API keys, or privileged tokens into Flutter or static assets.
- Do not trust client-provided roles, ownership, or publish state.
- Require Django-side authorization for content writes; current content writes belong in authenticated Django admin.
- Keep public API responses restricted to public/published data. The unrestricted settings response is tracked in `SECURITY_ROADMAP.md`.
- Use HTTPS in production and review server authorization even when a request claims to originate from the official client.

No claim is made that the web client is tamper-proof or that any client binary can be made impossible to reverse engineer.
