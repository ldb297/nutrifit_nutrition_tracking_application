from django.db import models
from datetime import date 
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'), 
    ('L', 'Lunch'), 
    ('D', 'Dinner'),
    ('S', 'Snack')
)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    kcals = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    sugars = models.FloatField()

    def __str__(self):
        return self.name

class Meal(models.Model):
    date = models.DateField('when you ate')
    meal = models.CharField(
        max_length=10,
        choices= MEALS,
        default= MEALS[0][0]
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return f"{self.user} had {self.meal} on {self.date}"