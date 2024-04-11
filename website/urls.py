from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("<str:page>", views.main_view, name="main"),
    path("page/<str:file>", views.page_view, name="page"),
]
