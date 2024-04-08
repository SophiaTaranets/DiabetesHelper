import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import authenticate, login, get_user_model
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
from .models import SugarLevelMeasure, User, SugarLevelList, Medicines
from .serializers import SugarLevelMeasureSerializer, UserSerializer, MealTimeChoiceSerializer, MedicinesSerializer, \
    SugarListSerializer, CreateUserSerializer


# to work with all measures
class SugarLevelMeasureList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]
    # serialize data of all measures to json
    serializer_class = SugarLevelMeasureSerializer

    # to display data in serialized format
    def get_queryset(self):
        return SugarLevelMeasure.objects.all()

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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # The redirect URI you set on Google - https://127.0.0.1:8000/accounts/google/login/callback/
    callback_url = 'http://127.0.0.1:8000/diabetes-helper/login/'
    client_class = OAuth2Client

    # def post(self, request, *args, **kwargs):
    #     # Check if 'code' parameter exists in the URL
    #     if 'code' in request.query_params:
    #         code = request.query_params['code']
    #         endpoint_url = 'https://127.0.0.1:8000/dj-rest-auth.google/'
    #         data = {"code": code}
    #         response = requests.post(endpoint_url, data=data)
    #         # Process the response as needed
    #         return Response(response.json(), status=response.status_code)
    #     else:
    #         # Redirect the user back to the login page or show an error message
    #         return HttpResponseRedirect('/login/')


