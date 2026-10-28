from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_homepage_cms'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='read_more_content',
            field=models.TextField(
                blank=True,
                help_text='Optional extra information shown when a visitor clicks [ Read ].',
                verbose_name='More to read',
            ),
        ),
    ]
