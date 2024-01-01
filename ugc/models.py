from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class TelegramUser(models.Model):
    tg_user_id = models.IntegerField(primary_key=True)
    tg_username = models.CharField(max_length=64)
    tg_user_lang = models.CharField(max_length=3)
    location_km = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(80)], default=80)
