from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0007_hero_panels'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinquiry',
            name='company_brand',
            field=models.CharField(blank=True, max_length=160, verbose_name='Company / brand'),
        ),
        migrations.AddField(
            model_name='contactinquiry',
            name='project_type',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='contactinquiry',
            name='budget_range',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
