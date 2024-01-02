from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_fsm import FSMField, transition


class TelegramUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    lang = models.CharField(max_length=3)
    registration_date = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='initial_state')

    @transition(field=state, source='initial_state', target='language_set')
    def set_language(self, language):
        self.lang = language
        self.save()


class TelegramUserSettings(models.Model):
    user_distance = models.IntegerField(
        validators=[MaxValueValidator(30), MinValueValidator(1)])
    telegram_user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE)


class Questionnaire(models.Model):
    user_profile = models.ImageField(
        upload_to="tg_user_profile/",
        null=True,
    )
    first_name = models.CharField(max_length=64)
    about_me = models.TextField(blank=True, null=True, default="")
    tg_user = models.OneToOneField(
        'TelegramUser',
        on_delete=models.CASCADE,
        related_name='ugc_questionnaire'
    )
