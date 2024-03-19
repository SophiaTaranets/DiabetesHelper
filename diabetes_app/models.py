from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    DIABETES_TYPES_CHOICES = {
        '1': 'First Type',
        '2': 'Second Type',
        '3': 'Gestational diabetes',
    }
    birth = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    diabetes_type = models.CharField(max_length=20, choices=DIABETES_TYPES_CHOICES, default='1')
    take_medicines = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='diabetes_users_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='diabetes_users_permissions',
        related_query_name='user',
    )


# automatically creates list for specific user
@receiver(post_save, sender=User)
def create_sugar_level_list(sender, instance, created, **kwargs):
    if created:
        SugarLevelList.objects.create(user_id=instance)


class SugarLevelList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class SugarLevelMeasure(models.Model):
    MEAL_TIME_CHOICES = {
        '1': 'Breakfast',
        '2': 'Brunch',
        '3': 'Snack',
        '4': 'Lunch',
        '5': 'Supper',
        '6': 'Dinner'
    }

    id = models.AutoField(primary_key=True, unique=True)
    sugar_list_id = models.ForeignKey(SugarLevelList, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    sugar_level = models.FloatField()
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES, default='1')
    carbs = models.FloatField(blank=True, null=True)
    proteins = models.FloatField(blank=True, null=True)
    fats = models.FloatField(blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class MedicinesList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Medicines(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=150)
    dose = models.FloatField()

    def __str__(self):
        return self.title
