from django.core.validators import FileExtensionValidator
from django.db import migrations, models
import django.db.models.deletion

import content.models


def create_default_panels(apps, schema_editor):
    HeroBranding = apps.get_model('content', 'HeroBranding')
    HeroPanel = apps.get_model('content', 'HeroPanel')
    database = schema_editor.connection.alias
    branding, _ = HeroBranding.objects.using(database).get_or_create(pk=1)
    HeroPanel.objects.using(database).bulk_create([
        HeroPanel(branding_id=branding.pk, slot=slot)
        for slot in range(1, 12)
    ], ignore_conflicts=True)


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0006_hero_logo_default_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroPanel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.PositiveSmallIntegerField(choices=[(1, 'Strip 1'), (2, 'Strip 2'), (3, 'Strip 3'), (4, 'Strip 4'), (5, 'Strip 5'), (6, 'Strip 6'), (7, 'Strip 7'), (8, 'Strip 8'), (9, 'Strip 9'), (10, 'Strip 10'), (11, 'Strip 11')], verbose_name='Strip position')),
                ('team_photo', models.ImageField(blank=True, help_text='Upload a JPG, PNG, or WebP image (maximum 8 MB). Leave empty for a plain white reverse side.', upload_to='site/hero-panels/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), content.models.validate_image_size], verbose_name='Team photo (optional)')),
                ('image_alt', models.CharField(blank=True, max_length=240, verbose_name='Photo description')),
                ('visible', models.BooleanField(default=True, verbose_name='Show this strip')),
                ('branding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='content.herobranding')),
            ],
            options={
                'verbose_name': 'homepage hero strip',
                'verbose_name_plural': 'homepage hero strips',
                'ordering': ['slot'],
                'constraints': [models.UniqueConstraint(fields=('branding', 'slot'), name='unique_hero_panel_slot')],
            },
        ),
        migrations.RunPython(create_default_panels, migrations.RunPython.noop),
    ]
