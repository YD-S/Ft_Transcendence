from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refresh/', views.refresh, name='refresh'),
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('me/', views.me, name='me'),
    path('2fa/', views.verify_2fa, name='verify_2fa'),
    path('resend-2fa/', views.resend_2fa_code, name='resend-2fa'),
    path('oauth/', views.oauth, name='oauth'),
    path('oauth_login/', views.oauth_login, name='oauth_login'),
]
