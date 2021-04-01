from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from .models import Meal, Ingredient
from .forms import MealForm, IngredientForm

class MealUpdate(UpdateView):
  model = Meal
  fields = ['date', 'meal']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/meals' + str(self.object.pk))

class MealDelete(DeleteView):
  model = Meal
  success_url = '/meals'


def index(request):
    return render(request, 'index.html')

#meals
@login_required()
def meals_index(request):
  # can access user through request
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
        'meal': str(x.get_meal_display()),
        'date': str(x.date),
        'ingredients': ingredient_list
      }
      meal_results.append(this_meal)
    return render(request, 'meals/index.html', { 'meals': meal_results })

@login_required()
def meals_show(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  ingredient_form = IngredientForm()
  return render(request, 'meals/show.html', {
    'meal': meal,
    'ingredient_form': ingredient_form
  })

def meals_update(request, pk):
  meal = Meal.objects.get(id=pk)
  meal_form = MealForm(meal)
  return render(request, 'meals/meal_form.html', {'form': meal_form})
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.save()
    return HttpResponseRedirect('/meals/' + str(self.object.pk))

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
  form = IngredientForm(request.POST)
  if form.is_valid():
    new_ingredient = form.save(commit=False)
    new_ingredient.meal_id = pk
    new_ingredient.save()
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
