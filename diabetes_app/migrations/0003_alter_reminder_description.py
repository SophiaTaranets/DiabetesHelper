# Generated by Django 4.2.11 on 2024-04-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_app', '0002_alter_user_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='description',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]