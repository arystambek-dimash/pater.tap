from django.contrib import admin
from .models import Photo, Post, Profile, Queries

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Profile)
admin.site.register(Queries)
