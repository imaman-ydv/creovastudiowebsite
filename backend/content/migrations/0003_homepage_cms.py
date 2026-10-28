from django.core.validators import FileExtensionValidator
from django.db import migrations, models

import content.models


def seed_homepage_content(apps, schema_editor):
    Service = apps.get_model('content', 'Service')
    Section = apps.get_model('content', 'SiteSectionVisibility')
    database = schema_editor.connection.alias

    cards = [
        {
            'slug': '3d-design-motion',
            'title': '3D Design & Motion',
            'description': 'We turn concepts into stunning 3D visuals and motion graphics that speak louder than words. Designed to inspire, engage, and connect instantly.',
            'details': 'From product showcases to brand films, our 3D and motion expertise adds depth, energy, and a modern edge. We help brands stand out with visuals that feel alive in today’s digital-first world.',
            'image_url': '/images/Poster12.avif',
            'image_alt': '3D design and motion graphics portfolio piece',
            'sort_order': 10,
        },
        {
            'slug': 'web-dev',
            'title': 'Web Dev',
            'description': 'We craft websites that don’t just look good—they work seamlessly. From clean code to smooth performance, we make sure every site is built for speed, security, and scalability.',
            'details': 'Our development process blends creativity with technology, turning ideas into powerful digital platforms that help brands grow and connect with their audience.',
            'image_url': '/images/Poster13.avif',
            'image_alt': 'Creative visual design by CreovaStudio',
            'sort_order': 20,
        },
        {
            'slug': 'films-ads',
            'title': 'Films & Ads',
            'description': 'We create compelling ad films that blend storytelling with stunning visuals, designed to grab attention and leave a lasting impression.',
            'details': 'From social media spots to full-scale commercials, our videos showcase brands in the most engaging and impactful way possible.',
            'image_url': '/images/Poster14.avif',
            'image_alt': 'Creative ad photography and visual storytelling',
            'sort_order': 30,
        },
        {
            'slug': 'digital-marketing',
            'title': 'Digital Marketing',
            'description': 'At Creova Studio, we don’t just build brands—we make them shine online. Our digital marketing services help you connect with the right audience, boost visibility, and drive real results.',
            'details': 'From social media to SEO, we make your brand shine online.',
            'image_url': '/images/Poster15.avif',
            'image_alt': 'Creative visual design by CreovaStudio',
            'sort_order': 40,
        },
        {
            'slug': 'graphic-designing',
            'title': 'Graphic Designing',
            'description': 'At Creova Studio, we believe design is the soul of communication. Our team blends creativity with precision to craft visuals that leave a lasting impact.',
            'details': 'From charcoal-style concepts to modern digital artwork, we create designs that speak without words and bring your ideas to life.',
            'image_url': '/images/Poster16.avif',
            'image_alt': 'Creative visual design by CreovaStudio',
            'sort_order': 50,
        },
    ]
    for card in cards:
        Service.objects.using(database).get_or_create(
            slug=card['slug'],
            defaults={**card, 'published': True, 'link_text': '[ Read ]', 'link_url': ''},
        )

    sections = [
        ('home-hero', 'Hero', 10),
        ('home-intro', 'Introduction', 20),
        ('home-latest-work', 'Latest work', 30),
        ('home-client-showcase', 'Client showcase', 40),
        ('home-services', 'Services and cards', 50),
    ]
    for key, label, order in sections:
        Section.objects.using(database).get_or_create(
            key=key,
            defaults={'label': label, 'page': 'Homepage', 'visible': True, 'sort_order': order},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_faqitem_service_sitepage_sitesetting_testimonial_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(
                help_text='The large title shown at the top of the card.',
                max_length=160,
                verbose_name='Card title',
            ),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(
                blank=True,
                help_text='The larger paragraph below the card title.',
                verbose_name='Main text',
            ),
        ),
        migrations.AlterField(
            model_name='service',
            name='details',
            field=models.TextField(
                blank=True,
                help_text='The smaller paragraph below the main text.',
                verbose_name='Supporting text',
            ),
        ),
        migrations.AlterField(
            model_name='service',
            name='image_url',
            field=models.CharField(
                blank=True,
                help_text='Existing image fallback. Upload a new image above to replace it.',
                max_length=500,
            ),
        ),
        migrations.AlterField(
            model_name='service',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Show this card'),
        ),
        migrations.AlterField(
            model_name='service',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Card position'),
        ),
        migrations.AddField(
            model_name='service',
            name='card_image',
            field=models.ImageField(
                blank=True,
                help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB).',
                upload_to='site/services/',
                validators=[
                    FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']),
                    content.models.validate_image_size,
                ],
                verbose_name='Card image',
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='image_alt',
            field=models.CharField(
                blank=True,
                help_text='Short description for accessibility.',
                max_length=240,
                verbose_name='Image description',
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='link_text',
            field=models.CharField(blank=True, default='[ Read ]', max_length=100, verbose_name='Link label'),
        ),
        migrations.AddField(
            model_name='service',
            name='link_url',
            field=models.CharField(blank=True, max_length=500, validators=[content.models.validate_public_link], verbose_name='Link destination'),
        ),
        migrations.AlterModelOptions(
            name='service',
            options={
                'ordering': ['sort_order', 'title'],
                'verbose_name': 'homepage card',
                'verbose_name_plural': 'homepage cards',
            },
        ),
        migrations.CreateModel(
            name='SiteSectionVisibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(editable=False, max_length=80, unique=True)),
                ('label', models.CharField(editable=False, max_length=120, verbose_name='Website section')),
                ('page', models.CharField(default='Homepage', editable=False, max_length=80)),
                ('visible', models.BooleanField(default=True, verbose_name='Show on website')),
                ('sort_order', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': 'website section',
                'verbose_name_plural': 'website sections',
                'ordering': ['sort_order', 'label'],
            },
        ),
        migrations.AlterModelOptions(
            name='contactinquiry',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'form submission',
                'verbose_name_plural': 'form submissions',
            },
        ),
        migrations.AlterField(
            model_name='contactinquiry',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Reviewed'),
        ),
        migrations.RunPython(seed_homepage_content, migrations.RunPython.noop),
    ]
