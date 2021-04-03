from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meals/', views.meals_index, name='meals'),
    path('meals/<int:meal_id>/', views.meals_show, name='meals_show'),
    path('meals/create/', views.meals_new, name='meals_create'),
    path('meals/<int:pk>/update/', views.meals_update, name='meals_update'),
    path('meals/<int:pk>/delete/', views.MealDelete.as_view(), name='meals_delete'),
    path('meals/<int:pk>/add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('meals/<int:meal_id>/delete_ingredient/<int:pk>', views.IngredientDelete.as_view(), name="delete_ingredient"),
    path('accounts/signup', views.sign_up, name='sign_up')
]
