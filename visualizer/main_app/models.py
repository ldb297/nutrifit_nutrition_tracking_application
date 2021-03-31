from django.db import models
from datetime import date 
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Meal(models.Model):
    date = models.DateField('when you ate')
    meal = models.CharField(
        max_length=1,
        choices= MEALS,
        default= MEALS[0][0]
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} had {self.meal} on {self.date}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100, default='None')
    kcals = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    sugars = models.IntegerField()

    meal = models.ManyToManyField(Meal)

    def __str__(self):
        return self.name