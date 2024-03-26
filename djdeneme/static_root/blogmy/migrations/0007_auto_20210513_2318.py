# Generated by Django 3.1.6 on 2021-05-13 20:18

import blogmy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmy', '0006_auto_20210513_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='myblogger',
            name='yayin_taslak',
            field=models.CharField(choices=[(None, 'Lütfen birini seçin'), ('yayin', 'YAYIN'), ('taslak', 'TASLAK')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='myblogger',
            name='image',
            field=models.ImageField(blank=True, default='deadpool_7.jpg', null=True, upload_to=blogmy.models.upload_to, verbose_name='Resim'),
        ),
    ]