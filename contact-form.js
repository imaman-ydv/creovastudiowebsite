(() => {
  document.addEventListener("submit", async (event) => {
    const form = event.target.closest("#contact-inquiry-form");
    if (!form) return;
    event.preventDefault();
    const submit = form.querySelector('button[type="submit"]');
    const status = form.querySelector("#inquiry-form-status");
    status.textContent = "";
    status.className = "inquiry-form__status";

    if (!form.reportValidity()) return;

    const fields = new FormData(form);
    const payload = Object.fromEntries(fields.entries());
    payload.website = fields.get("website") || "";
    submit.disabled = true;
    submit.querySelector("span").textContent = "Sending…";

    try {
      const response = await fetch("/api/contact/", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.error || "We couldn’t send your inquiry. Please try again.");

      form.reset();
      status.textContent = "Thanks for reaching out — we’ll be in touch soon.";
      status.classList.add("is--success");
    } catch (error) {
      status.textContent = error.message || "Something went wrong. Please try again or email us directly.";
      status.classList.add("is--error");
    } finally {
      submit.disabled = false;
      submit.querySelector("span").textContent = "Send inquiry";
    }
  });
})();
