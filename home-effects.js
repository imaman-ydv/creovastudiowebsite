(() => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    function setupHeadline() {
        const heading = document.querySelector(".home-hero__heading");
        if (!heading) return;
        heading.classList.add("home-heading-ready");
    }

    function setupSpotlight() {
        const visual = document.querySelector(".home-hero__visual");
        if (!visual || reduceMotion.matches || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

        const spotlight = document.createElement("span");
        spotlight.className = "home-hero__spotlight";
        spotlight.setAttribute("aria-hidden", "true");
        visual.append(spotlight);

        visual.addEventListener("pointermove", (event) => {
            const bounds = visual.getBoundingClientRect();
            spotlight.style.setProperty("--spot-x", `${event.clientX - bounds.left}px`);
            spotlight.style.setProperty("--spot-y", `${event.clientY - bounds.top}px`);
            visual.classList.add("has-pointer-spotlight");
        }, { passive: true });

        visual.addEventListener("pointerleave", () => {
            visual.classList.remove("has-pointer-spotlight");
        });
    }

    function setupScrollReveal() {
        const heading = document.querySelector("[data-heading-reveal].home-case__heading");
        const list = document.querySelector(".home-case__list");
        if (!heading && !list) return;

        if (!("IntersectionObserver" in window) || reduceMotion.matches) {
            heading?.classList.add("is-inview");
            list?.querySelectorAll(".home-case__item").forEach((item) => item.classList.add("is-inview"));
            return;
        }

        const observer = new IntersectionObserver((entries, currentObserver) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add("is-inview");
                currentObserver.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

        if (heading) observer.observe(heading);
        const observeItems = (root = document) => {
            root.querySelectorAll(".home-case__item:not(.is-inview)").forEach((item) => observer.observe(item));
        };
        observeItems(list || document);

        if (list) {
            const listObserver = new MutationObserver(() => observeItems(list));
            listObserver.observe(list, { childList: true, subtree: true });
        }
    }

    function init() {
        setupHeadline();
        setupSpotlight();
        setupScrollReveal();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();
