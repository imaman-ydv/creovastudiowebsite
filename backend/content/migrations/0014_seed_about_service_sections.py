from django.db import migrations


ABOUT_SECTIONS = [
    ('about-service-1-title', 'Brand Identity & Strategy', ''),
    ('about-service-1-body', '', 'We start by defining who you are. From naming and logo design to positioning and brand voice, we craft an identity that reflects your vision and resonates with your audience. Every brand needs a strong foundation, and we make sure yours stands out with clarity and purpose.'),
    ('about-service-2-title', 'Digital Presence & Experiences', ''),
    ('about-service-2-body', '', 'Your brand deserves to live where your audience is—online. We design and build websites, apps, and digital experiences that are not only visually striking but also seamless, functional, and engaging.'),
    ('about-service-3-title', 'Content Creation & Storytelling', ''),
    ('about-service-3-body', '', 'A brand is more than visuals—it’s the stories it tells. From high-quality photography and cinematic videos to creative campaigns and social media themes, we create content that sparks conversations and builds lasting connections with your audience.'),
    ('about-service-4-title', 'Growth & Market Activation', ''),
    ('about-service-4-body', '', 'Once the foundation is set, we help you scale. Whether it’s shaping go-to-market strategies, designing launch campaigns, or creating cultural moments, we ensure your brand grows with both commercial impact and cultural relevance—taking you from zero to 100.'),
    ('about-quote', '“We design with purpose—setting new standards for creativity, building meaningful connections, and driving measurable impact for brands and their audiences.”', ''),
]


def seed_about_services(apps, schema_editor):
    SitePage = apps.get_model('content', 'SitePage')
    PageSection = apps.get_model('content', 'PageSection')
    page = SitePage.objects.filter(slug='about').first()
    if not page:
        return
    for order, (key, heading, body) in enumerate(ABOUT_SECTIONS, start=30):
        PageSection.objects.get_or_create(
            page=page,
            content_key=key,
            defaults={'section_type': 'text', 'heading': heading, 'body': body, 'published': True, 'sort_order': order},
        )


class Migration(migrations.Migration):
    dependencies = [('content', '0013_seed_editable_pages')]
    operations = [migrations.RunPython(seed_about_services, migrations.RunPython.noop)]
