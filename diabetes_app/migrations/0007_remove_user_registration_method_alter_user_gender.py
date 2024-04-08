# Generated by Django 4.2.11 on 2024-04-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_app', '0006_user_registration_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='registration_method',
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=20),
        ),
    ]