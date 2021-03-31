from django.test import TestCase

# Create your tests here.
from main_app.models import Ingredient

class IngedientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name="Apple", kcals=10, carbs=20, fats=3, sugars=20)
        Ingredient.objects.create(name="Chicken", kcals=20, carbs=90, fats=13, sugars=3)

    def test_ingredient_names(self):
        """Ingredient that are identified by name"""
        apple = Cat.objects.get(name="Apple")
        chicken = Cat.objects.get(name="Chicken")
        
        self.assertEqual(apple.name, 'Apple')
        self.assertEqual(chicken.name, 'Chicken')
