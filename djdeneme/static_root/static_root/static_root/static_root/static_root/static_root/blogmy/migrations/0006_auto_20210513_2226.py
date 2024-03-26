# Generated by Django 3.1.6 on 2021-05-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmy', '0005_myblogger_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='myblogger',
            name='unique_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='myblogger',
            name='image',
            field=models.ImageField(blank=True, default='deadpool_7.jpg', null=True, upload_to='', verbose_name='Resim'),
        ),
    ]