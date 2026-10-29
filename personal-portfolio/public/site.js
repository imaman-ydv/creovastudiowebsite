const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav");

menuButton?.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isOpen));
  nav?.classList.toggle("is-open", !isOpen);
});

nav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuButton?.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  });
});

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});
