from rest_framework import serializers
from .models import Profile, Post, Queries, Photo
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'profile_photo', 'first_name', 'last_name', 'phone_number', 'contact_url']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'address', 'apartment_complex', 'room_quantity', 'description',
                  'price', 'additional_price', 'how_many_tenant_look', 'look_roommate', 'is_rented', 'expenses', 'user']


class QueriesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Queries
        fields = ['id', 'post', 'user']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'post']
