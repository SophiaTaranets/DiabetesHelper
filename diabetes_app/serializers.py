from rest_framework import serializers

from .models import SugarLevelMeasure, User, Medicines


class SugarLevelMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevelMeasure
        fields = ['date', 'time', 'sugar_level', 'meal_time', 'carbs', 'proteins', 'fats', 'calories', 'notes']


class MealTimeChoiceSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    sugar_level_list = SugarLevelMeasureSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields =['title', 'dose']
