from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import migrations, models

import content.models


def create_default_branding(apps, schema_editor):
    HeroBranding = apps.get_model('content', 'HeroBranding')
    HeroBranding.objects.using(schema_editor.connection.alias).get_or_create(
        pk=1,
        defaults={'image_alt': "CreovaStudio's Logo", 'size_percent': 100},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_service_read_more_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroBranding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_image', models.ImageField(
                    blank=True,
                    help_text='Upload a JPG, PNG, or WebP logo (maximum 8 MB). Leave empty to use the original logo.',
                    upload_to='site/branding/',
                    validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), content.models.validate_image_size],
                    verbose_name='Large homepage logo',
                )),
                ('image_alt', models.CharField(default="CreovaStudio's Logo", max_length=240, verbose_name='Image description')),
                ('size_percent', models.PositiveSmallIntegerField(
                    default=100,
                    help_text='100 fills the hero width. Use 30–100 to make the logo smaller. It stays centered.',
                    validators=[MinValueValidator(30), MaxValueValidator(100)],
                    verbose_name='Logo size (%)',
                )),
            ],
            options={
                'verbose_name': 'homepage hero logo',
                'verbose_name_plural': 'homepage hero logo',
            },
        ),
        migrations.RunPython(create_default_branding, migrations.RunPython.noop),
    ]
