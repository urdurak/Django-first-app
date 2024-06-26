# Generated by Django 3.1.6 on 2021-07-15 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('following', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='following',
            options={'verbose_name_plural': 'Takipleşme sistemi'},
        ),
        migrations.AlterField(
            model_name='following',
            name='follower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Takip eden Kullanıcı'),
        ),
    ]
