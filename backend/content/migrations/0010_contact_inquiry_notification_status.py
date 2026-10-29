from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0009_contact_inquiry_lead_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinquiry',
            name='notification_sent',
            field=models.BooleanField(default=False, verbose_name='Notification accepted by SMTP'),
        ),
    ]
