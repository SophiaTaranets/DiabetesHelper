from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """
       Custom user model manager where email is the unique identifiers
       for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
                Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)




class User(AbstractUser):
    DIABETES_TYPES_CHOICES = [
        ('1', 'First Type'),
        ('2', 'Second Type'),
        ('3', 'Gestational diabetes'),
    ]

    GENDER = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    # change default settings (register/login -> email)
    username = models.CharField(max_length=50)
    email = models.EmailField(('email address'), unique=True)

    birth = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, default=None)
    height = models.FloatField(null=True, default=None)
    gender = models.CharField(max_length=20, choices=GENDER, default='MALE')
    diabetes_type = models.CharField(max_length=20, choices=DIABETES_TYPES_CHOICES, default='1', null=False, blank=False)
    take_medicines = models.BooleanField(default=True)
    # auth_method = models.CharField(
    #     max_length=255,
    #     blank=False,
    #     null=False,
    #     choices=AUTH_CHOICES,
    #     default='email'
    # )

    # change default settings (register/login -> email)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Reminder(models.Model):
    REMINDER_TIME_CHOICES = [
        ('1', 'Breakfast'),
        ('2', 'Brunch'),
        ('3', 'Snack'),
        ('4', 'Lunch'),
        ('5', 'Supper'),
        ('6', 'Dinner'),
    ]

    REMINDER_DAY_CHOICES = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Friday'),
    ]

    title = models.CharField(max_length=20, choices=REMINDER_TIME_CHOICES, default='1')
    description = models.TextField(max_length=250, null=True, blank=True)
    day = models.CharField(max_length=25, choices=REMINDER_DAY_CHOICES, default='1')
    due_time = models.TimeField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# automatically creates list for specific user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_sugar_level_list(sender, instance, created, **kwargs):
    if created:
        SugarLevelList.objects.create(user_id=instance)


# automatically creates token for specific user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class SugarLevelList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class SugarLevelMeasure(models.Model):
    MEAL_TIME_CHOICES = [
        ('1', 'Breakfast'),
        ('2', 'Brunch'),
        ('3', 'Snack'),
        ('4', 'Lunch'),
        ('5', 'Supper'),
        ('6', 'Dinner'),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    sugar_list_id = models.ForeignKey(SugarLevelList, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
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
    dose = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.title
