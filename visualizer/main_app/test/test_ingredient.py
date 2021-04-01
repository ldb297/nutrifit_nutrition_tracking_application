from django.test import TestCase

# Create your tests here.
from main_app.models import User, Ingredient, Meal

class IngedientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='Apple', kcals=10, carbs=20, fats=3, sugars=20)
        Ingredient.objects.create(name='Chicken', kcals=20, carbs=90, fats=13, sugars=3)

    def test_ingredient_names(self):
        """Ingredient that are identified by name"""
        apple = Ingredient.objects.get(name='Apple')
        chicken = Ingredient.objects.get(name='Chicken')
        
        self.assertEqual(apple.name, 'Apple')
        self.assertEqual(chicken.name, 'Chicken')

class MealTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='testUser')
        Meal.objects.create(date='2021-03-31', meal='B', user_id=1)
        Meal.objects.create(date='2021-03-31', meal='L', user_id=1)

    def test_meal_dates(self):
        """Meal dates inputted correctly"""
        todays_breakfast = Meal.objects.get(date='2021-03-31', meal='B')
        todays_lunch = Meal.objects.get(date='2021-03-31', meal='L')

        self.assertEquals(todays_breakfast.date, '2021, 03, 31')
        self.assertEquals(todays_lunch.date, '2021, 03, 31')