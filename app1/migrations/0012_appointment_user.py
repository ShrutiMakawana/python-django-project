# Generated by Django 5.0.3 on 2024-04-28 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_appointment_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]
