# Generated by Django 3.1.7 on 2021-03-31 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='meal',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='meal',
            field=models.ManyToManyField(to='main_app.Meal'),
        ),
    ]
