from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SugarLevelList, SugarLevelMeasure, MedicinesList, Medicines

# admin.site.register(User, UserAdmin)
admin.site.register(SugarLevelList)
admin.site.register(SugarLevelMeasure)
admin.site.register(MedicinesList)
admin.site.register(Medicines)


class EmailUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'birth', 'gender')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, EmailUserAdmin)
