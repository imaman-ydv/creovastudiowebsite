# Aman Yadav Portfolio

This is a standalone personal portfolio for Aman Yadav, built for the Creova Studio Docker Compose stack. It uses a custom editorial “paper, ink and signal” design, an original cute Three.js robot with glass accents and an SVG fallback, and three Creova project thumbnails. It does not include the separately licensed `Portfolio-Website` source, its proprietary 3D model, or its visual assets.

The Express app runs as the `personal-portfolio` Compose service and is served by the company site at `/portfolio/`. Start the regular stack from the repository root with:

```sh
docker compose up --build -d
```

Open `http://localhost:8080/portfolio/`. No separate portfolio command or exposed host port is needed.
