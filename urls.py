from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.index,name='home'),
    path('', views.about,name='about'),
    path('', views.service,name='services'),
]
