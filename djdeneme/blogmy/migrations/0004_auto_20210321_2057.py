# Generated by Django 3.1.6 on 2021-03-21 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogmy', '0003_auto_20210321_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myblogger',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]
