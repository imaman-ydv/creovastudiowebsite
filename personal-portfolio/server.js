import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

const app = express();
const port = Number(process.env.PORT || 3000);
const appDir = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(appDir, "public");

app.disable("x-powered-by");
app.use("/vendor/three", express.static(path.join(appDir, "node_modules/three/build")));
app.use(express.static(publicDir, { extensions: ["html"] }));
app.get("/health", (_request, response) => response.status(200).send("ok"));
app.use((_request, response) => response.status(404).sendFile(path.join(publicDir, "404.html")));

app.listen(port, "0.0.0.0", () => {
  console.log(`Aman Yadav portfolio listening on ${port}`);
});
