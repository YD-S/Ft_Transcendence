from django.shortcuts import redirect
from django.urls import path

from . import views

urlpatterns = [
    path("2fa/<int:user_id>", views.two_factor_auth, name="2fa"),
    path("<str:page>", views.main_view, name="main"),
    path("page/<str:file>", views.page_view, name="page"),
]
