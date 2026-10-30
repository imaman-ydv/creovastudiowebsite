const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

menuButton?.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isOpen));
  menuButton.textContent = isOpen ? "Menu" : "Close";
  nav?.classList.toggle("is-open", !isOpen);
});

const closeMenu = () => {
  menuButton?.setAttribute("aria-expanded", "false");
  if (menuButton) menuButton.textContent = "Menu";
  nav?.classList.remove("is-open");
};

nav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

const headingItems = [...document.querySelectorAll(".hero h1 > span, .about-content h2, .focus-card h3, .work-heading h2, .experience-grid h2, .contact-section h2")];
headingItems.forEach((heading, index) => {
  heading.classList.add("heading-reveal", "reveal");
  if (heading.matches(".hero h1 > span")) heading.style.setProperty("--heading-delay", `${index * 95}ms`);
});

const revealItems = [...document.querySelectorAll(".reveal")];
if (!reduceMotion && "IntersectionObserver" in window && revealItems.length) {
  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      currentObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -36px 0px" });
  document.documentElement.classList.add("js-ready");
  revealItems.forEach((item) => observer.observe(item));
}
