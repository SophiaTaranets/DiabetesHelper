from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import SugarLevelMeasureList, UserList, MealChoicesList, MedicinesList

urlpatterns = [
    path('measures/', SugarLevelMeasureList.as_view()),
    path('meals/',   MealChoicesList.as_view()),
    path('medicines/', MedicinesList.as_view()),
    path('users/', UserList.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
