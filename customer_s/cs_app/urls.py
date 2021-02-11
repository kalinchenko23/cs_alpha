from django.contrib import admin
from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('',views.home),
    re_path(r'saw_something/$',views.saw_something),
    re_path(r'pt_schedule/$',views.pt_schedule)
]