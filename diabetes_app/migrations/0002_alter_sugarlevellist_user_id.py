# Generated by Django 5.0.3 on 2024-03-19 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sugarlevellist',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='diabetes_app.user'),
        ),
    ]
