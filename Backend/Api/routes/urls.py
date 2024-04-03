from django.urls import include, path


urlpatterns = [
    path('user/', include(("users.urls", "users"), namespace="users")),
]
