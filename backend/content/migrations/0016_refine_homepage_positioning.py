from django.db import migrations


SERVICE_COPY = {
    '3d-design-motion': {
        'title': '3D Design & Motion',
        'description': 'Bring products and ideas to life with expressive 3D, motion and animation that make people stop and look.',
        'details': 'Product visuals, 3D animation, VFX and motion graphics.',
        'read_more_content': 'We create polished 3D assets and motion-led stories for launches, campaigns and digital experiences. From a single product visual to a complete brand film, every frame is made to hold attention.',
    },
    'web-dev': {
        'title': 'Web & App Development',
        'description': 'Digital experiences designed around your customers—and built to perform across every screen.',
        'details': 'Websites, ecommerce, landing pages and custom digital products.',
        'read_more_content': 'We bring design and engineering together to build fast, accessible digital products. From a focused campaign page to a full ecommerce or web platform, the experience stays clear and easy to use.',
    },
    'films-ads': {
        'title': 'Films & Ads',
        'description': 'Campaign films and social content that tell your story with purpose and visual impact.',
        'details': 'Brand films, product videos, social edits and motion-led ads.',
        'read_more_content': 'We shape concepts, production and post into memorable films for brands. The result is content designed for the way people watch, share and discover stories today.',
    },
    'digital-marketing': {
        'title': 'Digital Marketing',
        'description': 'Connect with the right people through clear strategy and content built for the channels they use.',
        'details': 'Social media, SEO, campaign creative and performance assets.',
        'read_more_content': 'We help brands plan and create consistent digital campaigns, from channel strategy and social content to SEO and performance creative. Every piece works toward a clear business goal.',
    },
    'graphic-designing': {
        'title': 'Graphic Design',
        'description': 'Make every message clearer with visual design that keeps your brand distinctive and consistent.',
        'details': 'Campaign assets, editorial design, presentations and marketing collateral.',
        'read_more_content': 'We design practical, polished visual systems for everyday brand communication. From campaign graphics to presentations and editorial layouts, each asset feels part of the same story.',
    },
}


def refine_homepage(apps, schema_editor):
    database = schema_editor.connection.alias
    Service = apps.get_model('content', 'Service')
    PageSection = apps.get_model('content', 'PageSection')

    placeholder = Service.objects.using(database).filter(slug='test').first()
    if placeholder and not Service.objects.using(database).filter(slug='branding-identity').exists():
        placeholder.slug = 'branding-identity'
        placeholder.title = 'Branding & Identity'
        placeholder.description = 'Build a clear, distinctive brand—from the strategy behind it to the visual identity people remember.'
        placeholder.details = 'Positioning, naming, identity systems and launch assets.'
        placeholder.read_more_content = 'We align your positioning, voice and visual identity so every touchpoint feels consistent—from the first impression to the full brand system your team can use.'
        placeholder.image_alt = 'Branded apparel and ecommerce identity concept'
        placeholder.sort_order = 5
        placeholder.save()

    for slug, copy in SERVICE_COPY.items():
        Service.objects.using(database).filter(slug=slug).update(**copy)

    sections = {
        'home-hero-heading': {'heading': 'One partner. Every digital move.'},
        'home-intro-copy-one': {
            'body': 'Creova Studio brings strategy, design and technology under one roof. We build the digital foundations ambitious brands need—from identity and websites to content, campaigns and immersive visuals.'
        },
        'home-intro-copy-two': {
            'body': 'One connected team means fewer handoffs, clearer thinking and a more consistent brand everywhere it shows up. Tell us what you’re building; we’ll bring the right mix of creative and technical skills.'
        },
        'home-services-heading': {'heading': 'Digital, done together.'},
        'home-services-intro': {
            'body': 'From brand identity and websites to content, motion and marketing, we bring every part of your digital presence together.'
        },
    }
    for key, fields in sections.items():
        PageSection.objects.using(database).filter(content_key=key).update(**fields)


class Migration(migrations.Migration):
    dependencies = [('content', '0015_seed_homepage_content')]

    operations = [migrations.RunPython(refine_homepage, migrations.RunPython.noop)]
