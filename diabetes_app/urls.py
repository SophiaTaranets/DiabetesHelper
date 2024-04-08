from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token

from .views import SugarLevelMeasureList, MealChoicesList, MedicinesList, LoginView, SugarList, RegisterView, \
    GoogleLogin

urlpatterns = [
    path('measures/', SugarLevelMeasureList.as_view()),
    path('sugar-list/', SugarList.as_view()),
    path('meals/',   MealChoicesList.as_view()),
    path('medicines/', MedicinesList.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    # path("dj-rest-auth/google/login/", GoogleLoginView.as_view())

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
