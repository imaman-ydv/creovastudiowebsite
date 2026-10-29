from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0011_insight_cover_image_insight_image_alt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insight',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
