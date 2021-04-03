from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from .models import Meal, Ingredient
from .forms import MealForm, IngredientForm, ApiForm

import requests

API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query="

# def api(request):
#   ingredient_form = IngredientForm()
#   user_meals = list(request.user.meal_set.all())
#   print(user_meals)
#   if request.POST:
#     api_form = ApiForm()
#     keyword = request.POST.get('name')
#     response = requests.get(f"{API_URL}{keyword}&pageSize=25")
#     response = response.json()
#     nutrients = response['foods'][0]['foodNutrients']
#     for x in nutrients:
#       if x['nutrientId'] == 1003:
#         protein = x['value']
#       elif x['nutrientId'] == 1004:
#         fats = x['value']
#       elif x['nutrientId'] == 1005:
#         carbs = x['value']
#       elif x['nutrientId'] == 1008:
#         kcals = x['value']
#       elif x['nutrientId'] == 2000:
#         sugars = x['value']
#     nutrient_stats = {
#       'name': keyword,
#       'protein': protein,
#       'kcals': kcals,
#       'carbs': carbs,
#       'fats': fats,
#       'sugars': sugars
#       }
#     return render(request, 'api.html', { 'api_form': api_form, 'ingredient': nutrient_stats, 'ingredient_form':ingredient_form, 'user_meals':user_meals })
#   api_form = ApiForm()
#   return render(request, 'api.html', { 'api_form': api_form, 'user_meals':user_meals })

def index(request):
    user = request.user
    user_meals = len(user.meal_set.all())
    return render(request, 'index.html', { 'user': user, 'meals': user_meals })

#meals
@login_required()
def meals_index(request):
    meal_results = []
    result = Meal.objects.filter(user = request.user)
    for x in result:
      ingredients = x.ingredients.all()
      ingredient_list = []
      for y in ingredients:
        ingredient_list.append({
          'name': y.name,
          'kcals': y.kcals,
          'carbs': y.carbs,
          'fats': y.fats,
          'sugars': y.sugars,
          'id': y.id
        })
      this_meal = {
        'id': x.id,
        'meal': str(x.get_meal_display()),
        'date': str(x.date),
        'ingredients': ingredient_list
      }
      meal_results.append(this_meal)
    return render(request, 'meals/index.html', { 'meals': meal_results })

@login_required()
def meals_show(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  ingredients = meal.ingredients.all()
  ingredient_list = []
  for x in ingredients:
    ingredient = {
      'id': x.id,
      'name': x.name,
      'kcals': x.kcals,
      'carbs': x.carbs,
      'fats': x.fats,
      'sugars': x.sugars,
    }
    ingredient_list.append(ingredient)
  ingredient_form = IngredientForm()
  api_form = ApiForm()
  nutrient_stats = {}
  if request.POST:
    api_form = ApiForm()
    keyword = request.POST.get('name')
    response = requests.get(f"{API_URL}{keyword}&pageSize=25")
    response = response.json()
    nutrients = response['foods'][0]['foodNutrients']
    for x in nutrients:
      if x['nutrientId'] == 1003:
        protein = x['value']
      elif x['nutrientId'] == 1004:
        fats = x['value']
      elif x['nutrientId'] == 1005:
        carbs = x['value']
      elif x['nutrientId'] == 1008:
        kcals = x['value']
      elif x['nutrientId'] == 2000:
        sugars = x['value']
    nutrient_stats = {
      'name': keyword,
      'protein': protein,
      'kcals': kcals,
      'carbs': carbs,
      'fats': fats,
      'sugars': sugars
      }
  return render(request, 'meals/show.html', {
    'meal': meal,
    'ingredients': ingredient_list,
    'ingredient_form': ingredient_form,
    'ingredient': nutrient_stats,
    'api_form': api_form
  })

def meals_update(request, pk):
  if request.POST:
    meal = Meal.objects.get(id=pk)
    meal.date = request.POST.get('date')
    meal.meal = request.POST.get('meal')
    meal.save()
    return redirect('meals')
  else:
    meal = Meal.objects.get(id=pk)
    meal_form = MealForm(instance=meal)
    return render(request, 'meals/meal_form.html', {'form': meal_form})

class MealDelete(DeleteView):
  model = Meal
  success_url = '/meals'

class IngredientDelete(DeleteView):
  model = Ingredient
  success_url = '/meals'

@login_required()
def meals_new(request):
  meal_form = MealForm(request.POST or None)
  if request.POST and meal_form.is_valid():
    new_meal = meal_form.save(commit=False)
    new_meal.user = request.user
    new_meal.save()
    return redirect('index')
  else:
    return render(request, 'meals/new.html', {'meal_form': meal_form})

@login_required()
def add_ingredient(request, pk):
  meal = Meal.objects.get(id=pk)
  form = IngredientForm(request.POST)
  if form.is_valid():
    new_ingredient = form.save(commit=False)
    new_ingredient.save()
    meal.ingredients.add(new_ingredient)
  return redirect('meals_show', meal_id = pk)

def sign_up(request):
  error_message= ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      #user creation ok, log em in
      login(request, user)
      return redirect('index')
    else:
      error_message='invalid sign up, please try again'
  #if !POST or !valid
  form = UserCreationForm()
  return render(request, 'registration/signup.html', { 
    'form':form, 
    'error_message': error_message
    })
