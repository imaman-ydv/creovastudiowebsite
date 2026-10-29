from django.db import migrations


HOME_SECTIONS = [
    ('home-hero-heading', 'Turning Imagination Into Reality', '', '', '', ''),
    ('home-intro-label', '[ Intro ]', '', '', '', ''),
    ('home-intro-copy-one', '', 'Creova Studio is a creative and technology-driven digital agency dedicated to helping brands unlock their true potential in the online world. With a deep focus on design, development, and innovation, we craft tailored digital solutions that not only look stunning but also deliver measurable impact. Our expertise spans across web development, branding, UI/UX design, e-commerce, and digital experiences—ensuring that every project reflects both creativity and precision.', '', '', ''),
    ('home-intro-image-one', '', '', '/images/Poster11.avif', '', ''),
    ('home-intro-copy-two', '', 'At Creova Studio, we believe in merging art with technology to create meaningful digital experiences that inspire, engage, and empower. Every idea we take on is shaped with strategy, innovation, and attention to detail, helping businesses build stronger connections with their audience. We are more than just developers or designers—we are partners in growth, working relentlessly to transform visions into reality.', '', '', ''),
    ('home-intro-image-two', '', '', '/images/Poster4.avif', '', ''),
    ('home-intro-sticker', '', '', '/animationLogo/1.png', '', ''),
    ('home-work-heading', 'Latest work', '', '', '', ''),
    ('home-featured-link', '', '', '', './krishadha.html', 'View the featured project'),
    ('home-featured-image', '', '', '/images/Krishadha1.avif', '', ''),
    ('home-featured-title', 'Krishadha', '', '', '', ''),
    ('home-featured-summary', 'Where Royalty Finds that Its Attire', '', '', '', ''),
    ('home-work-button', '', '', '', './work.html', 'Straight outta our creative lab'),
    ('home-client-heading', 'Beyond Clients, Allies.', '', '', '', ''),
    ('home-client-sticker', '', '', '/images/67629a606926bd7c54141d0a_sticker.avif', '', ''),
    ('home-services-heading', 'What We Excel At In', '', '', '', ''),
    ('home-services-intro', '', 'At Creova Studio, we excel in bringing ideas to life through stunning visuals and cutting-edge creativity. From high-impact video editing, 3D design, VFX, and animation to professional brand photoshoots, we craft experiences that inspire, engage, and elevate every project.', '', '', ''),
]


def seed_homepage(apps, schema_editor):
    SitePage = apps.get_model('content', 'SitePage')
    PageSection = apps.get_model('content', 'PageSection')
    page, _ = SitePage.objects.get_or_create(
        slug='home', defaults={'title': 'Homepage', 'published': True, 'sort_order': 0}
    )
    for order, (key, heading, body, image_url, link_url, link_text) in enumerate(HOME_SECTIONS):
        PageSection.objects.get_or_create(
            page=page,
            content_key=key,
            defaults={
                'section_type': 'image' if image_url else 'text',
                'heading': heading,
                'body': body,
                'image_url': image_url,
                'link_url': link_url,
                'link_text': link_text,
                'published': True,
                'sort_order': order,
            },
        )


class Migration(migrations.Migration):
    dependencies = [('content', '0014_seed_about_service_sections')]
    operations = [migrations.RunPython(seed_homepage, migrations.RunPython.noop)]
