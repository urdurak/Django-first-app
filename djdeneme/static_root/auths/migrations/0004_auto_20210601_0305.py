# Generated by Django 3.1.6 on 2021-06-01 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_auto_20210601_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(choices=[(None, 'Lütfen Birini Seçin'), ('hicbiri', 'Belirtmek İstemiyorum'), ('erkek', 'ERKEK'), ('kadın', 'KADIN')], max_length=22, null=True, verbose_name='Cinsiyet'),
        ),
    ]