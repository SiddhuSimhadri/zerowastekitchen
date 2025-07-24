from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.waste_stats, name='waste_stats'),
]
