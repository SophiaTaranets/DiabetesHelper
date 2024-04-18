from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from . import google
from .models import SugarLevelMeasure, User, Medicines, SugarLevelList


class SugarLevelMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevelMeasure
        fields = ['date', 'time', 'sugar_level', 'meal_time', 'carbs', 'proteins', 'fats', 'calories', 'notes']


class SugarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevelList
        fields = '__all__'


class MealTimeChoiceSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    # sugar_level_list = SugarLevelMeasureSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'birth', 'weight', 'height',
                  'gender', 'diabetes_type', 'take_medicines', 'first_name')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields =['title', 'dose']


# class GoogleAuthSerializer(serializers.Serializer):
#     auth_token = serializers.CharField()
#
#     def validate_auth_token(self, auth_token):
#         user_data = google.Google.validate(auth_token)
#         try:
#             user_data['sub']
#         except:
#             raise serializers.ValidationError(
#                 'Incorrect token. Please login again.'
#             )
#
#         if user_data['aud'] != '73000166296-uj0lk401sde8b5vq1glqbr2lftrv6vbd.apps.googleusercontent.com':
#             raise AuthenticationFailed('oops, who are you?')
#
#         user_id = user_data['sub']
#         email = user_data['email']
#         username=user_data['name']
#         provider = user_data['google']
#
#         return register_social_user(
#             provider=provider,
#             user_id=user_id,
#             email=email,
#             username=username
#         )


