from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    contact_url = models.CharField(max_length=100, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    apartment_complex = models.CharField(max_length=100, blank=True)
    room_quantity = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.IntegerField()
    additional_price = models.IntegerField(blank=True, null=True)
    how_many_tenant_look = models.IntegerField(blank=True, null=True)
    look_roommate = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)
    expenses = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Queries(models.Model):
    flat = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    image = models.ImageField(upload_to='flat_photos')
    flat = models.ForeignKey(Post, on_delete=models.CASCADE)
