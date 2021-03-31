from django import forms
from .models import Eating

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'kcals', 'carbs', 'fats', 'sugars', 'meal']