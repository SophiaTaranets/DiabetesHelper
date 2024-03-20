from django.shortcuts import render
from rest_framework import generics

from .models import SugarLevelMeasure, User, SugarLevelList, Medicines
from .serializers import SugarLevelMeasureSerializer, UserSerializer, MealTimeChoiceSerializer, MedicinesSerializer


# to work with all measures
class SugarLevelMeasureList(generics.ListCreateAPIView):

    # serialize data of all measures to json
    serializer_class = SugarLevelMeasureSerializer

    # to display data in serialized format
    def get_queryset(self):
        return SugarLevelMeasure.objects.all()

    def perform_create(self, serializer):
        # get sugar_list of the user
        sugar_list = self.get_user_sugar_list()

        # bind this list to future measures
        serializer.save(sugar_list_id=sugar_list)

    # get id of sugar_level_list for the specific user to add measures to specific list

    # ADD AUTHENTICATION TO DISTINGUISH USERS!!!!
    def get_user_sugar_list(self):
        # HARDCODE
        sugar_list_id = 1
        try:
            sugar_list = SugarLevelList.objects.get(id=sugar_list_id)
        except SugarLevelList.DoesNotExist:
            sugar_list = None
        return sugar_list


class MealChoicesList(generics.ListAPIView):
    # get meals data from db as a list of tuples ('1', 'breakfast'...)
    queryset = SugarLevelMeasure.MEAL_TIME_CHOICES.items()
    serializer_class = MealTimeChoiceSerializer

    # add logic to change tuples to dict using keys
    def get_queryset(self):
        return [{'key': key, 'value': value} for key, value in self.queryset]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MedicinesList(generics.ListAPIView):
    queryset = Medicines.objects.all()
    serializer_class = MedicinesSerializer
