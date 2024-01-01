from django.contrib import admin
from .models import Photo, Flat, Questionnaire, AdditionalDetail, Contact

admin.site.register(Flat)
admin.site.register(Photo)
admin.site.register(Questionnaire)
admin.site.register(AdditionalDetail)
admin.site.register(Contact)
