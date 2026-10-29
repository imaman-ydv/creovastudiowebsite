from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0008_contact_inquiry_project_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinquiry',
            name='status',
            field=models.CharField(
                choices=[('new', 'New'), ('in_progress', 'In progress'), ('won', 'Won'), ('lost', 'Lost')],
                default='new',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='contactinquiry',
            name='internal_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contactinquiry',
            name='follow_up_at',
            field=models.DateField(blank=True, null=True, verbose_name='Follow-up date'),
        ),
    ]
