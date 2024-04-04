from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refresh/', views.refresh, name='refresh'),
]
