from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refresh/', views.refresh, name='refresh'),
    path('register/', views.register, name='refresh'),
    path('change_password/', views.change_password, name='refresh'),
]
