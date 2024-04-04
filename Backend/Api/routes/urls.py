from django.urls import include, path


urlpatterns = [
    path('user/', include(("users.urls", "users"), namespace="users")),
    path('auth/', include(("authentication.urls", "authentication"), namespace="authentication")),
]
