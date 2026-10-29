(function () {
  const api = (path) => fetch(`/api/${path}`).then((response) => {
    if (!response.ok) throw new Error(`Content API returned ${response.status}`);
    return response.json();
  });

  const setText = (node, value) => {
    if (node && typeof value === 'string' && value.trim()) node.textContent = value;
  };

  function renderStory(host, body, images) {
    const story = document.createElement('div');
    story.className = 'article w-richtext cms-story';
    body.split(/\n\s*\n/).map((part) => part.trim()).filter(Boolean).forEach((part) => {
      const paragraph = document.createElement('p');
      paragraph.textContent = part;
      story.appendChild(paragraph);
    });
    (images || []).forEach((item) => {
      if (!item.image_url) return;
      const figure = document.createElement('figure');
      const image = document.createElement('img');
      image.src = item.image_url;
      image.alt = item.image_alt || '';
      image.loading = 'lazy';
      image.style.width = '100%';
      image.style.height = 'auto';
      figure.appendChild(image);
      if (item.caption) {
        const caption = document.createElement('figcaption');
        caption.textContent = item.caption;
        figure.appendChild(caption);
      }
      story.appendChild(figure);
    });
    if (host.matches('.article.w-richtext')) host.replaceChildren(...story.childNodes);
    else host.replaceChildren(story);
  }

  async function hydratePage(main) {
    const slug = main.dataset.cmsPage;
    if (slug === 'about') {
      const page = await api('pages/about/');
      page.sections.forEach((section) => {
        if (!section.key) return;
        const target = main.querySelector(`[data-cms-key="${CSS.escape(section.key)}"]`);
        if (!target) return;
        setText(target, section.heading);
        if (section.body) setText(target, section.body);
        if (section.image_url && target.matches('img')) {
          target.src = section.image_url;
          target.alt = section.image_alt || target.alt;
        }
      });
      return;
    }

    if (slug === 'work') {
      const { results } = await api('projects/');
      const bySlug = new Map(results.map((project) => [project.slug, project]));
      main.querySelectorAll('.work-page__item').forEach((card, index) => {
        const href = card.querySelector('a[href]')?.getAttribute('href') || '';
        const file = href.split('/').pop()?.replace(/\.html$/, '');
        const project = bySlug.get(file);
        if (!project) return;
        setText(card.querySelector('.work-page__title h2'), project.title);
        setText(card.querySelector('.work-page__bottom-des p'), project.summary);
        setText(card.querySelector('.work-page__bottom .force'), project.year ? String(project.year) : '');
        const image = card.querySelector('.work-page__img img');
        if (image && project.cover_image_url) {
          image.src = project.cover_image_url;
          image.alt = project.image_alt || project.title;
        }
        const hiddenImage = main.querySelectorAll('[data-work-img="hidden"] img')[index];
        if (hiddenImage && project.cover_image_url) hiddenImage.src = project.cover_image_url;
      });
      return;
    }

    const projectSlug = main.dataset.cmsProject;
    if (projectSlug) {
      const project = await api(`projects/${encodeURIComponent(projectSlug)}/`);
      main.querySelectorAll('.h-case').forEach((title) => setText(title, project.title));
      main.querySelectorAll('.case-hero .flex-h, .case-hero__sub .flex-h').forEach((yearRow) => {
        setText(yearRow.querySelectorAll('.eyebrow-r')[1], project.year ? String(project.year) : '');
      });
      const categoryLines = (project.category || '').split(/\s*\/\s*/).filter(Boolean);
      main.querySelectorAll('.case-hero__details').forEach((category) => {
        const lines = category.querySelectorAll('p');
        if (lines.length) lines.forEach((line, index) => setText(line, categoryLines[index] || ''));
        else setText(category, project.category);
      });
      main.querySelectorAll('.case-hero .align-bottom.right > p.eyebrow-r, .case-hero__sub .align-bottom.right > p.eyebrow-r')
        .forEach((summary) => setText(summary, project.summary));
      const heroImage = main.querySelector('.case-hero ~ .bg img, .full-height__inner .bg img, .case-hero img');
      if (heroImage && project.cover_image_url) {
        heroImage.src = project.cover_image_url;
        heroImage.alt = project.image_alt || project.title;
      }
      if (project.body) {
        const contentRows = [...main.querySelectorAll('.case-row')].filter((row) => !row.classList.contains('case-hero'));
        contentRows.forEach((row) => { row.hidden = true; });
        const section = document.createElement('section');
        section.className = 'section cms-story-section';
        section.innerHTML = '<div class="container"><div class="content-row"><div class="content-col"></div></div></div>';
        renderStory(section.querySelector('.content-col'), project.body, project.images);
        const hero = main.querySelector('.case-hero')?.closest('section');
        if (hero) hero.after(section);
      }
      return;
    }

    const insightSlug = main.dataset.cmsInsight;
    if (insightSlug) {
      const insight = await api(`insights/${encodeURIComponent(insightSlug)}/`);
      setText(main.querySelector('.heading-article'), insight.title);
      if (insight.excerpt) {
        const meta = document.querySelector('meta[name="description"]');
        if (meta) meta.content = insight.excerpt;
      }
      if (insight.published_at) {
        const date = main.querySelector('.author-row .eyebrow-r');
        if (date) setText(date, new Date(insight.published_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }));
      }
      const heroImage = main.querySelector('.article-hero img');
      if (heroImage && insight.cover_image_url) {
        heroImage.src = insight.cover_image_url;
        heroImage.alt = insight.image_alt || insight.title;
      }
      if (insight.body) {
        const content = main.querySelector('.article.w-richtext');
        if (content) renderStory(content, insight.body, insight.images);
      }
    }
  }

  const initialize = () => {
    const main = document.querySelector('main[data-cms-page], main[data-cms-project], main[data-cms-insight]');
    if (!main || main.dataset.cmsHydrated === 'yes') return;
    main.dataset.cmsHydrated = 'yes';
    hydratePage(main).catch((error) => console.warn('CMS content unavailable; keeping the original page.', error));
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
  new MutationObserver(initialize).observe(document.documentElement, { childList: true, subtree: true });
})();
