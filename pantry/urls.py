from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Home page after login
    path('add/', views.add_pantry_item, name='add_pantry_item'),
]
