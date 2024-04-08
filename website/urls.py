from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:page>", views.main_view, name="main"),
    path("page/<str:file>", views.page_view, name="page"),
]
