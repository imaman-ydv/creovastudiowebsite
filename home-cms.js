(function () {
    const servicesList = document.querySelector('[data-cms-services-list]');
    let readDialog;

    function getReadDialog() {
        if (readDialog) return readDialog;

        const dialog = document.createElement('dialog');
        dialog.className = 'service-read-dialog';

        const header = document.createElement('div');
        header.className = 'service-read-dialog__header';
        const title = document.createElement('h2');
        title.className = 'service-read-dialog__title';
        title.id = 'service-read-dialog-title';
        const close = document.createElement('button');
        close.className = 'service-read-dialog__close';
        close.type = 'button';
        close.textContent = 'Close ×';
        close.addEventListener('click', () => dialog.close());
        header.append(title, close);

        const content = document.createElement('div');
        content.className = 'service-read-dialog__content';
        dialog.setAttribute('aria-labelledby', title.id);
        dialog.append(header, content);
        dialog.addEventListener('click', (event) => {
            if (event.target === dialog) dialog.close();
        });
        document.body.append(dialog);

        readDialog = { dialog, title, content };
        return readDialog;
    }

    function openReadDialog(service, opener) {
        const { dialog, title, content } = getReadDialog();
        title.textContent = service.title || '';
        content.replaceChildren();

        if (service.image_url) {
            const image = document.createElement('img');
            image.className = 'service-read-dialog__image';
            image.src = service.image_url;
            image.alt = service.image_alt || service.title || '';
            content.append(image);
        }

        [service.description, service.details, service.read_more_content]
            .filter((value) => value && value.trim())
            .forEach((value) => {
                const paragraph = document.createElement('p');
                paragraph.textContent = value;
                content.append(paragraph);
            });

        dialog.addEventListener('close', function restoreFocus() {
            dialog.removeEventListener('close', restoreFocus);
            if (opener && opener.isConnected) opener.focus();
        });
        dialog.showModal();
    }

    function safeLink(value) {
        if (!value || value === '#') return '#';
        if (value.startsWith('/') && !value.startsWith('//')) return value;

        try {
            const url = new URL(value, window.location.origin);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '#';
        } catch (_error) {
            return '#';
        }
    }

    function updateAnimatedText(target, value) {
        const lineWraps = target.querySelectorAll('.single-line-wrap');
        const lines = target.querySelectorAll('.single-line');
        if (!lines.length) {
            target.textContent = value;
            return;
        }

        lines[0].textContent = value;
        lineWraps.forEach((wrap, index) => { wrap.hidden = index > 0; });
        target.setAttribute('aria-label', value);
    }

    async function loadHomePageContent() {
        try {
            const response = await fetch('/api/pages/home/', { cache: 'no-store' });
            if (!response.ok) return;
            const page = await response.json();
            (page.sections || []).forEach((section) => {
                if (!section.key) return;
                const target = document.querySelector(`[data-cms-key="${CSS.escape(section.key)}"]`);
                if (!target) return;

                if (target.matches('img') && section.image_url) {
                    target.src = section.image_url;
                    target.removeAttribute('srcset');
                    target.removeAttribute('sizes');
                    target.alt = section.image_alt || target.alt || '';
                    return;
                }

                const text = section.heading || section.body;
                if (text && text.trim()) updateAnimatedText(target, text);
                if (target.matches('a') && section.link_url) target.href = safeLink(section.link_url);
                if (target.matches('a') && section.link_text) {
                    const label = target.querySelector('.h-reg, .h-xsmall, .h-small');
                    if (label) label.textContent = section.link_text;
                    target.setAttribute('aria-label', section.link_text);
                }
            });
        } catch (_error) {
            // Keep the original homepage copy and images if the CMS is unavailable.
        }
    }

    async function loadHeroBranding() {
        const logo = document.querySelector('[data-cms-hero-logo]');
        if (!logo) return;

        try {
            const response = await fetch('/api/branding/', { cache: 'no-store' });
            if (!response.ok) return;
            const branding = await response.json();
            if (branding.logo_url) logo.src = branding.logo_url;
            logo.alt = branding.image_alt || "CreovaStudio's Logo";
            const requestedSize = Number(branding.size_percent);
            const size = Number.isFinite(requestedSize) ? Math.min(100, Math.max(30, requestedSize)) : 86;
            logo.style.setProperty('--cms-hero-logo-size', `${size}%`);
        } catch (_error) {
            // Keep the original centered logo if the branding API is unavailable.
        }
    }

    function setupHeroPanels() {
        const overlay = document.querySelector('[data-cms-hero-panels]');
        if (!overlay) return;

        const panels = Array.from(overlay.querySelectorAll(':scope > .visual-col'));
        const resetPanels = () => {
            panels.forEach((panel) => {
                panel.classList.remove('is-flipped');
                panel.setAttribute('aria-pressed', 'false');
            });
        };
        const activatePanel = (activePanel) => {
            panels.forEach((panel) => {
                const isActive = panel === activePanel;
                panel.classList.toggle('is-flipped', isActive);
                panel.setAttribute('aria-pressed', String(isActive));
            });
        };
        const panelViews = panels.map((panel, index) => {
            const front = document.createElement('div');
            front.className = 'visual-col__front';
            // The source columns contain GSAP-driven decorative fragments. They
            // obscure a full-card flip, so each panel gets one clean black face.
            front.replaceChildren();

            const back = document.createElement('div');
            back.className = 'visual-col__back';
            back.setAttribute('aria-hidden', 'true');

            const inner = document.createElement('div');
            inner.className = 'visual-col__flip';
            inner.append(front, back);
            panel.append(inner);
            panel.classList.add('visual-col--interactive');
            panel.classList.remove('md--hide');
            panel.dataset.heroPanelSlot = String(index + 1);
            panel.setAttribute('role', 'button');
            panel.setAttribute('tabindex', '0');
            panel.setAttribute('aria-pressed', 'false');
            panel.setAttribute('aria-label', `Flip hero strip ${index + 1}`);

            panel.addEventListener('pointerenter', (event) => {
                if (event.pointerType === 'mouse') activatePanel(panel);
            });
            panel.addEventListener('click', () => activatePanel(panel));
            panel.addEventListener('keydown', (event) => {
                if (event.key !== 'Enter' && event.key !== ' ') return;
                event.preventDefault();
                panel.click();
            });

            return { panel, back };
        });

        const heroVisual = overlay.closest('.home-hero__visual');
        heroVisual?.addEventListener('pointerleave', (event) => {
            if (event.pointerType === 'mouse') resetPanels();
        });

        fetch('/api/hero-panels/', { cache: 'no-store' })
            .then((response) => response.ok ? response.json() : Promise.reject(new Error('Hero panels unavailable')))
            .then((payload) => {
                const contentBySlot = new Map((payload.results || []).map((item) => [Number(item.slot), item]));
                panelViews.forEach(({ panel, back }, index) => {
                    const content = contentBySlot.get(index + 1);
                    if (!content) return;

                    panel.hidden = !content.visible;
                    if (!content.visible) return;
                    if (content.image_url) {
                        const image = document.createElement('img');
                        image.src = content.image_url;
                        image.alt = content.image_alt || '';
                        image.loading = 'lazy';
                        back.append(image);
                        panel.setAttribute('aria-label', content.image_alt || `Flip hero strip ${index + 1}`);
                    }
                });
            })
            .catch(() => {
                // Keep the original hero strips interactive with white backs if CMS data is unavailable.
            });
    }

    function renderServiceCard(service, template) {
        const card = template.cloneNode(true);
        card.classList.remove('active');
        card.removeAttribute('style');
        card.dataset.cmsService = service.slug || '';
        card.cmsServiceData = service;

        const link = card.querySelector('a.article-slide');
        link.href = safeLink(service.link_url);
        link.setAttribute('aria-label', service.title || 'Homepage card');

        const titleRow = card.querySelector('.article-slide__content .flex-h');
        const titleTemplate = titleRow.querySelector('.h-xlarge');
        const title = titleTemplate.cloneNode(false);
        title.textContent = service.title || '';
        title.style.whiteSpace = 'pre-line';
        titleRow.replaceChildren(title);

        const content = card.querySelector('.article-slide__content');
        const description = content.querySelector('h3');
        description.textContent = service.description || '';

        const details = content.querySelector('p.eyebrow-r');
        details.textContent = service.details || '';
        details.hidden = !service.details;

        const image = card.querySelector('.article-slide__img img');
        const imageBox = card.querySelector('.article-slide__img');
        image.removeAttribute('srcset');
        image.removeAttribute('sizes');
        if (service.image_url) {
            image.src = service.image_url;
            imageBox.hidden = false;
        } else {
            image.removeAttribute('src');
            imageBox.hidden = true;
        }
        image.alt = service.image_alt || service.title || '';

        const cardBottom = card.querySelector('.article-slide__bottom');
        const readLabel = cardBottom.querySelector('[data-lines-hover]');
        const label = service.link_text || '[ Read ]';
        const visibleReadLabel = cardBottom.querySelector('.single-line');
        if (visibleReadLabel) {
            visibleReadLabel.textContent = label;
            readLabel.textContent = '';
            const readTrigger = visibleReadLabel.closest('.single-line-wrap');
            if (readTrigger) {
                readTrigger.setAttribute('role', 'button');
                readTrigger.tabIndex = 0;
                readTrigger.setAttribute('aria-label', `Read more about ${service.title || 'this service'}`);
            }
        } else {
            readLabel.textContent = label;
            readLabel.setAttribute('role', 'button');
            readLabel.tabIndex = 0;
        }

        return card;
    }

    async function loadServices() {
        if (!servicesList) return;

        try {
            const response = await fetch('/api/services/', { cache: 'no-store' });
            if (!response.ok) return;
            const payload = await response.json();
            if (!Array.isArray(payload.results)) return;

            const template = servicesList.querySelector('.article-slide__wrap');
            if (!template) return;

            const cards = payload.results.map((service) => renderServiceCard(service, template));
            servicesList.replaceChildren(...cards);
            servicesList.style.touchAction = 'pan-x pan-y';

            if (!servicesList.dataset.readMoreReady) {
                servicesList.dataset.readMoreReady = 'true';
                servicesList.addEventListener('click', (event) => {
                    const card = event.target.closest('.article-slide__wrap');
                    if (!card || !card.cmsServiceData) return;
                    const trigger = event.target.closest('.single-line-wrap[role="button"], [data-lines-hover][role="button"]');
                    if (!trigger && card.cmsServiceData.link_url) return;
                    event.preventDefault();
                    event.stopPropagation();
                    openReadDialog(card.cmsServiceData, trigger || card.querySelector('a.article-slide'));
                });
                servicesList.addEventListener('keydown', (event) => {
                    if (event.key !== 'Enter' && event.key !== ' ') return;
                    const trigger = event.target.closest('.single-line-wrap[role="button"], [data-lines-hover][role="button"]');
                    if (!trigger) return;
                    const card = trigger.closest('.article-slide__wrap');
                    if (!card || !card.cmsServiceData) return;
                    event.preventDefault();
                    event.stopPropagation();
                    openReadDialog(card.cmsServiceData, trigger);
                });
            }

            const sliderViewport = document.querySelector('[data-cms-services-slider] .w-dyn-list');
            const controls = document.querySelector('[data-cms-services-controls]');
            if (sliderViewport) {
                sliderViewport.tabIndex = 0;
                sliderViewport.setAttribute('role', 'region');
                sliderViewport.setAttribute('aria-label', 'Service cards. Use left and right arrow keys to browse.');
            }
            if (sliderViewport && controls) {
                controls.querySelectorAll('[data-slider="prev"], [data-slider="next"]').forEach((button) => {
                    button.addEventListener('click', () => {
                        const firstCard = servicesList.querySelector('.article-slide__wrap');
                        if (!firstCard) return;
                        const gap = Number.parseFloat(getComputedStyle(servicesList).columnGap) || 0;
                        const distance = firstCard.getBoundingClientRect().width + gap;
                        sliderViewport.scrollBy({
                            left: button.dataset.slider === 'next' ? distance : -distance,
                            behavior: 'smooth',
                        });
                    });
                });
            }

            const slider = document.querySelector('[data-cms-services-slider]');
            if (slider) slider.hidden = cards.length === 0;
            if (controls) controls.hidden = cards.length === 0;
        } catch (_error) {
            // Keep the original static cards visible if the content API is unavailable.
        }
    }

    async function loadSectionVisibility() {
        try {
            const response = await fetch('/api/sections/', { cache: 'no-store' });
            if (!response.ok) return;
            const payload = await response.json();
            if (!Array.isArray(payload.results)) return;

            const visibility = new Map(payload.results.map((section) => [section.key, section.visible]));
            document.querySelectorAll('[data-cms-section]').forEach((element) => {
                const state = visibility.get(element.dataset.cmsSection);
                if (state !== undefined) element.hidden = !state;
            });
        } catch (_error) {
            // Keep all original sections visible if the content API is unavailable.
        }
    }

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        const slider = event.target.closest('[data-cms-services-slider]');
        if (!slider) return;
        const viewport = slider.querySelector('.w-dyn-list');
        const firstCard = servicesList && servicesList.querySelector('.article-slide__wrap');
        if (!viewport || !firstCard) return;
        const gap = Number.parseFloat(getComputedStyle(servicesList).columnGap) || 0;
        const distance = firstCard.getBoundingClientRect().width + gap;
        viewport.scrollBy({
            left: event.key === 'ArrowRight' ? distance : -distance,
            behavior: 'smooth',
        });
        event.preventDefault();
    });

    setupHeroPanels();
    loadHeroBranding();
    loadHomePageContent();
    loadServices();
    loadSectionVisibility();
}());
