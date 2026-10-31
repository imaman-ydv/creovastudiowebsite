from django.db import migrations


SERVICE_IMAGES = {
    'branding-identity': ('/images/services/branding-identity.jpg', 'Colorful brand identity packaging and stationery concept'),
    '3d-design-motion': ('/images/services/3d-motion.jpg', 'Colorful abstract 3D motion sculpture'),
    'web-dev': ('/images/services/web-app.jpg', 'Responsive website and mobile app concept'),
    'films-ads': ('/images/services/films-ads.jpg', 'Cinema camera on a warmly lit film set'),
    'digital-marketing': ('/images/services/digital-marketing.jpg', 'Colorful social media campaign and audience concept'),
    'graphic-designing': ('/images/services/graphic-design.jpg', 'Colorful graphic design posters and palette'),
}


def add_service_images(apps, schema_editor):
    database = schema_editor.connection.alias
    Service = apps.get_model('content', 'Service')
    for slug, (image_url, image_alt) in SERVICE_IMAGES.items():
        Service.objects.using(database).filter(slug=slug).update(
            image_url=image_url,
            image_alt=image_alt,
        )


class Migration(migrations.Migration):
    dependencies = [('content', '0016_refine_homepage_positioning')]

    operations = [migrations.RunPython(add_service_images, migrations.RunPython.noop)]
