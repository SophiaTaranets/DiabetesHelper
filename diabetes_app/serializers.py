from rest_framework import serializers

from .models import SugarLevelMeasure, User


class SugarLevelMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevelMeasure
        fields = ['date', 'time', 'sugar_level', 'meal_time', 'carbs', 'proteins', 'fats', 'calories', 'notes']


class UserSerializer(serializers.ModelSerializer):
    sugar_level_list = SugarLevelMeasureSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
