# Generated by Django 5.0 on 2024-01-01 16:35

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_remove_telegramuser_location_km'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuser',
            old_name='tg_user_lang',
            new_name='lang',
        ),
        migrations.RenameField(
            model_name='telegramuser',
            old_name='tg_user_id',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='telegramuser',
            old_name='tg_username',
            new_name='username',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile', models.ImageField(null=True, upload_to='tg_user_profile/')),
                ('first_name', models.CharField(max_length=64)),
                ('about_me', models.TextField(blank=True, default='', null=True)),
                ('tg_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ugc_questionnaire', to='ugc.telegramuser')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_distance', models.IntegerField(default=30, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)])),
                ('telegram_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ugc.telegramuser')),
            ],
        ),
    ]
