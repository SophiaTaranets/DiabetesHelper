from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from . import google
from .models import SugarLevelMeasure, User, Medicines, SugarLevelList, Reminder


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

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'day', 'due_time']

class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields =['title', 'dose']

