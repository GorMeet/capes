# Generated by Django 4.0.3 on 2022-06-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_scheduledmail_schedule_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledmail',
            name='status',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]