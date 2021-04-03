from django import forms
from .models import Meal, Ingredient

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'protein', 'kcals', 'carbs', 'fats', 'sugars']

class ApiForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name']