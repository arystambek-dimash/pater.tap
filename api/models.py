from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from ugc.models import TelegramUser


class Photo(models.Model):
    image = models.ImageField(upload_to='flat_photos/', blank=True, null=True)
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE, related_name='photos')


class Flat(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    apartment_complex = models.CharField(max_length=255)
    room_quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    description = models.TextField(max_length=512)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    how_many_tenant_look = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    look_roommate = models.BooleanField(default=False)

    is_rented = models.BooleanField(default=False)
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, blank=True, null=True)
    contact = models.OneToOneField("Contact", on_delete=models.CASCADE, blank=True, null=True)
    additional_detail = models.OneToOneField("AdditionalDetail", on_delete=models.CASCADE, null=True, blank=True)


class AdditionalDetail(models.Model):
    building_material = models.CharField(max_length=255, blank=True, null=True)
    area_of_house = models.IntegerField(blank=True, null=True)
    number_of_floors = models.IntegerField(null=True, blank=True)
    year_of_constuction = models.IntegerField(null=True, blank=True)
    condition_house = models.CharField(max_length=50, default="Good")


class Questionnaire(models.Model):
    contact = models.OneToOneField("Contact", on_delete=models.CASCADE)
    about_me = models.CharField(max_length=255)
    tg_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        null=True,
        blank=True
    )
