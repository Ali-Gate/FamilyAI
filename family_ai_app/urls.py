from django.urls import path
from . import views


app_name = 'family_ai_app'
# The app_name is used to create namespaced URLs for the app.


# The urlpatterns list routes URLs to views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
