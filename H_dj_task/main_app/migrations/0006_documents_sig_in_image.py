# Generated by Django 3.1.3 on 2020-11-16 13:44

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20201116_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='sig_in_image',
            field=models.ImageField(default=None, null=True, upload_to=main_app.models.doc_file_path),
        ),
    ]
