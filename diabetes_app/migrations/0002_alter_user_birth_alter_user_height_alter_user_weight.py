# Generated by Django 5.0.3 on 2024-03-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.FloatField(default=None, null=True),
        ),
    ]
