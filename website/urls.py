from django.urls import path

from . import views


urlpatterns = [
    path("page/<path:file>", views.page_view, name="page"),
    path("<path:page>", views.main_view, name="main"),
]
