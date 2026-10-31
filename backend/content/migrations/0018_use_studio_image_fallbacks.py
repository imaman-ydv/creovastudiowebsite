from django.db import migrations


SERVICE_SLUGS = (
    'branding-identity',
    '3d-design-motion',
    'web-dev',
    'films-ads',
    'digital-marketing',
    'graphic-designing',
)


def use_studio_fallbacks(apps, schema_editor):
    database = schema_editor.connection.alias
    Service = apps.get_model('content', 'Service')
    Service.objects.using(database).filter(slug__in=SERVICE_SLUGS).update(card_image='')


class Migration(migrations.Migration):
    dependencies = [('content', '0017_add_colorful_home_service_images')]

    operations = [migrations.RunPython(use_studio_fallbacks, migrations.RunPython.noop)]
