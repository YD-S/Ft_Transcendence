from django.urls import include, path

from users.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('<int:pk>/', UserViewSet.as_view(detail=True)),
]
