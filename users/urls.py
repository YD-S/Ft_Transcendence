from django.urls import include, path

from users.views import UserViewSet, TournamentViewSet, BlockedUserViewSet

urlpatterns = [
    path('', UserViewSet.as_view()),
    path('<int:pk>/', UserViewSet.as_view(detail=True)),
    path('tournament/', TournamentViewSet.as_view()),
    path('tournament/<int:pk>', TournamentViewSet.as_view(detail=True)),
    path('blocked/', BlockedUserViewSet.as_view()),
    path('blocked/<int:pk>', BlockedUserViewSet.as_view(detail=True)),
]
