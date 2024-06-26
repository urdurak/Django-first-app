# Generated by Django 3.1.6 on 2021-06-07 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogmy', '0011_myblogger_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myblogger',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Gönderiler'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='isim',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='soyisim',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='icerik',
            field=models.TextField(max_length=300, null=True, verbose_name='Yorum'),
        ),
    ]
