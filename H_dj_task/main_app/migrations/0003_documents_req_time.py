# Generated by Django 3.1.2 on 2020-11-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20201114_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='req_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
