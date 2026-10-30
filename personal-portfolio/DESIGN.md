# Aman Yadav · Independent creative engineer

## 0. Brief

Build a one-page personal portfolio for Aman Yadav, founder of Creova Studio. Visitors are prospective collaborators and clients who want to understand his creative and technical work quickly.

**Aesthetic:** tactile, editorial, technical, optimistic.

**Signature:** an original cute Three.js robot with a polished cream shell, friendly signal-orange eyes and ears, a translucent glass antenna and orbital accents. It floats/turns gently and follows the pointer across the full window, beside a large four-line statement. A hand-drawn SVG robot remains as a no-WebGL fallback.

**Scope:** responsive single-page profile with About, Capabilities, Selected Work, Experience and Contact sections. Keep claims tied to the supplied profile content. Keep links to the company site and case studies functional.

## 1. Stack and assets

- Existing Express static app; keep the current Docker Compose `/portfolio/` mount.
- Vanilla HTML, CSS and JavaScript with Three.js for the hero scene only.
- Keep the original inline SVG sculpture as the fallback. Use the three supplied Creova project images in `public/projects/`.
- No MotionSites media shelf assets, licensed model, stock photographs, or external font dependencies.

## 2. Tokens

| Role | Value |
|---|---|
| Paper | `#f1ede4` |
| Light paper | `#f8f5ed` |
| Ink | `#171715` |
| Muted | `#716e67` |
| Night | `#161716` |
| Signal accent | `#ff6542` |
| Body | system sans, 15–18px, 1.55–1.65 line-height |
| Display | Impact / Arial Narrow fallback, uppercase, tight leading |
| Labels | system monospace, 9–10px, uppercase, tracked |
| Content | max-width 1440px, 20px mobile gutters, 56px desktop gutters |

Use the accent for the sculpture details, action links and section indices. No ambient gradients or decorative blobs. A restrained grain overlay ties the paper and dark art panel together.

## 3. Composition

- Header is a compact wordmark and four quiet links; mobile uses a 44px menu button.
- Desktop hero is an asymmetrical two-column spread: copy on the left, a dark technical art panel on the right. The hero statement is set in four explicit lines: “I make / digital / things / matter.”
- The art panel uses a fine grid, inset keyline, faint outline “AY”, orbit rings, micro-labels, and the procedural cute robot sculpture. Pointer input across the page gives it a restrained position and rotation response; touch devices use its slow ambient motion.
- Capability cards, art labels, and project controls use a restrained frosted-glass treatment, with visible borders and readable contrast.
- About is an open two-column editorial section. Capabilities are three numbered columns on a single dark field. Project cards use the real case-study artwork and link to the corresponding company case pages. Experience is a ruled timeline; Contact is a dark, type-led closing panel.

## 4. Motion and accessibility

- Hero copy enters with a short upward fade, staggered by 120ms.
- The sculpture floats and turns slowly while orbit rings drift. Pointer input anywhere in the page eases the sculpture toward the cursor; touch devices do not run pointer tracking.
- Hovering or focusing “Let’s talk” makes the robot switch to its friendly smiling expression. A large cursive robot prompt and circular orange arrow sit below the link; tapping it triggers a celebratory wave, floating sparkles, and “Thank you for believing in me!”
- Hero headline lines animate in with a short stagger. Section headings reveal upward with a slight blur when they enter view.
- Project artwork scales to 1.045 over 750ms on hover. Scroll reveals run once at a 12% viewport threshold.
- The SVG fallback remains visible if Three.js or WebGL is unavailable. `prefers-reduced-motion` disables entrances, orbit animation, scene movement and smooth scrolling.
- Provide visible focus states, descriptive image alt text, meaningful link labels, and 44px mobile menu controls.

## 5. Responsive acceptance

- At 1440px: hero fits within the first viewport, with legible copy and an unobstructed sculpture.
- At 768px: hero stacks, keeps the art below the headline, and cards remain readable.
- At 375px: no horizontal overflow; four-line display headline stays inside the viewport; nav opens and closes by button, link and Escape.
- Contact email, company link, and all three project case-study links remain operable.

## 6. Build review

Follow the relevant MotionSites Web Builder workflow: define a specific art direction, use one signature interaction, preserve responsive and reduced-motion behavior, capture desktop and mobile screenshots, and fix visible layout or asset failures. Reference: [Motionsites-AI/claude-skill](https://github.com/Motionsites-AI/claude-skill). Its example prompts and media remain copyrighted; this portfolio uses none of those assets.
