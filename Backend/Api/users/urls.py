from django.urls import include, path

from users.views import UserViewSet

urlpatterns = [
    path('', include(UserViewSet().as_urls())),
]
