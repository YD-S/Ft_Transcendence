from django.urls import path

from . import views

urlpatterns = [
    path("", views.generic("index.html"), name="index"),
    path("home", views.generic("home.html"), name="index"),
    path("settings", views.generic("settings.html"), name="settings"),
    path("multiplayer", views.generic("multiplayer.html"), name="settings"),
]
