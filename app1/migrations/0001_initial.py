# Generated by Django 5.0.3 on 2024-04-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=70)),
                ('age', models.IntegerField(default=0)),
                ('mobileno', models.CharField(default='', max_length=10)),
                ('email', models.EmailField(default='', max_length=254)),
                ('service', models.CharField(default='', max_length=100)),
                ('date', models.DateField()),
                ('slot', models.TextField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=30)),
                ('subject', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('emp_id', models.BigAutoField(default=0, primary_key=True, serialize=False)),
                ('emp_name', models.CharField(default='', max_length=70)),
                ('emp_designation', models.CharField(default='', max_length=120)),
                ('emp_description', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.BigAutoField(default=1, primary_key=True, serialize=False)),
                ('service_name', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
