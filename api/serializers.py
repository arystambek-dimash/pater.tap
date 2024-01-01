from rest_framework import serializers
from api.models import *


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class AdditionalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalDetail
        fields = '__all__'


class FlatSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False, read_only=True)
    additional_detail = AdditionalDetailSerializer(required=False, read_only=True)
    contact = ContactSerializer(required=False, read_only=True)

    class Meta:
        model = Flat
        fields = '__all__'

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        additional_detail_data = validated_data.pop('additional_detail', {})
        contact_data = validated_data.pop('contact', {})
        additional_instance = AdditionalDetail.objects.create(**additional_detail_data)
        contact_instance = Contact.objects.create(**contact_data)

        flat = Flat.objects.create(contact=contact_instance, additional_detail=additional_instance, **validated_data)

        for photo_data in photos_data:
            Photo.objects.create(flat=flat, **photo_data)

        return flat


class QuestionnaireSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = Questionnaire
        fields = '__all__'
