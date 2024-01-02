# Generated by Django 5.0 on 2024-01-01 18:08

import django.core.validators
import django_fsm
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0005_rename_tg_user_lang_telegramuser_lang_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='state',
            field=django_fsm.FSMField(default='initial_state', max_length=50),
        ),
        migrations.AlterField(
            model_name='telegramusersettings',
            name='user_distance',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)]),
        ),
    ]
