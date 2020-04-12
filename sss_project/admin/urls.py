from django.urls import path
from admin import views

app_name = 'admins'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('get_code/', views.get_code, name='get_code'),
    path('check_user/', views.check_user, name='check_user'),


]