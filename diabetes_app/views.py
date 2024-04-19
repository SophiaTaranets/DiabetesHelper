import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from rest_framework import generics, views, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .models import SugarLevelMeasure, User, SugarLevelList, Medicines, Reminder
from .serializers import SugarLevelMeasureSerializer, UserSerializer, MealTimeChoiceSerializer, MedicinesSerializer, \
    SugarListSerializer, CreateUserSerializer, ReminderSerializer
from django.core.mail import send_mail, EmailMessage
import smtplib

# to work with all measures
class SugarLevelMeasureList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    # serialize data of all measures to json
    serializer_class = SugarLevelMeasureSerializer

    # to display data in serialized format
    def get_queryset(self):
        queryset = SugarLevelMeasure.objects.all()
        user_pk = self.request.user.pk

        return queryset.filter(sugar_list_id_id=user_pk)

    def perform_create(self, serializer):
        # get sugar_list of the user
        sugar_list = self.get_user_sugar_list(self.request.data['user_id'])

        # bind this list to future measures
        serializer.save(sugar_list_id=sugar_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # get id of sugar_level_list for the specific user to add measures to specific list

    # ADD AUTHENTICATION TO DISTINGUISH USERS!!!!
    def get_user_sugar_list(self, user_id):
        # HARDCODE
        try:
            sugar_list = SugarLevelList.objects.get(user_id=user_id)
        except SugarLevelList.DoesNotExist:
            sugar_list = None
        return sugar_list

    # def post(self, request, *args, **kwargs):
    #     sugar_list_id = self.get_user_sugar_list(request.data['user_id'])
    #     serializer = self.get_serializer(sugar_list_id=sugar_list_id)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserSugarLevelMeasure(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SugarLevelMeasureSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def get_queryset(self):
        queryset = SugarLevelMeasure.objects.all()
        measure_pk = self.kwargs['pk']

        return queryset.filter(id=measure_pk)

class MealChoicesList(generics.ListAPIView):
    # get meals data from db as a list of tuples ('1', 'breakfast'...)
    queryset = SugarLevelMeasure.MEAL_TIME_CHOICES
    serializer_class = MealTimeChoiceSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # add logic to change tuples to dict using keys
    def get_queryset(self):
        return [{'key': key, 'value': value} for key, value in self.queryset]


class SugarList(generics.ListAPIView):
    queryset = SugarLevelList.objects.all()
    serializer_class = SugarListSerializer


class UserSugarList(generics.RetrieveUpdateAPIView):
    serializer_class = SugarListSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user_pk = self.kwargs['pk']
        return SugarLevelList.objects.filter(user_id=user_pk)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReminderList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    # serialize data of all measures to json
    serializer_class = ReminderSerializer

    # to display data in serialized format
    def get_queryset(self):
        queryset = Reminder.objects.all()
        user_pk = self.request.user.pk

        return queryset.filter(user_id=user_pk)

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.pk

        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReminderItem(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    # serialize data of all measures to json
    serializer_class = ReminderSerializer

    # to display data in serialized format
    def get_queryset(self):
        queryset = Reminder.objects.all()
        reminder_id = self.kwargs['pk']

        return queryset.filter(id=reminder_id)



@csrf_exempt
def send_welcome_email(request):
    email = EmailMessage(
        'Title',
        'Thank you for creating an account!',
        'olegshevchenko806@gmail.com',
        ['sony.taranets@gmail.com']
    )

    email.send()
    # subject = 'Sugar Measure Reminder'
    # message = 'Thank you for creating an account!'
    # from_email = 'olegshevchenko806@gmail.com'
    # recipient_list = ['sony.taranets@gmail.com']
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class MedicinesList(generics.ListAPIView):
    queryset = Medicines.objects.all()
    serializer_class = MedicinesSerializer


# send credentials to check user and get token/id
class LoginView(ObtainAuthToken):
    # to render data(to json) from this view
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class RegisterView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    # @csrf_exempt
    def post(self, *args, **kwargs):
        serializer = CreateUserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


