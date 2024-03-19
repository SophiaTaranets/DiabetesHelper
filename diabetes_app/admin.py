from django.contrib import admin

from .models import User, SugarLevelList, SugarLevelMeasure, MedicinesList, Medicines

admin.site.register(User)
admin.site.register(SugarLevelList)
admin.site.register(SugarLevelMeasure)
admin.site.register(MedicinesList)
admin.site.register(Medicines)
