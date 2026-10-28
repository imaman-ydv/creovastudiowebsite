from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


def reduce_initial_full_size_logo(apps, schema_editor):
    HeroBranding = apps.get_model('content', 'HeroBranding')
    HeroBranding.objects.using(schema_editor.connection.alias).filter(size_percent=100).update(size_percent=86)


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_homepage_hero_branding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herobranding',
            name='size_percent',
            field=models.PositiveSmallIntegerField(
                default=86,
                help_text='Choose 30–100% of the hero area. The default 86% leaves space around the logo; it stays centered.',
                validators=[
                    MinValueValidator(30),
                    MaxValueValidator(100),
                ],
                verbose_name='Logo size (%)',
            ),
        ),
        migrations.RunPython(reduce_initial_full_size_logo, migrations.RunPython.noop),
    ]
