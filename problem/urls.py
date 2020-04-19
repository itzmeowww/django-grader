from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('problem/<int:pk>/', views.ProblemDetail, name='problem'),
]
