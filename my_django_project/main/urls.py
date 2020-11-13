"""my_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('', views.index, name='Home'),
    path('login', views.login, name='Login'),
    path('new_user', views.new_user, name='SignUp'),
    path('profile', views.profile_user, name='Profile'),
    path('user', views.user, name='UserPage'),
    path('user/list', views.user_list, name='UserList'),
    path('user/profit', views.user_profit, name='Profit'),
    path('contacts', views.contacts, name='Contacts'),
    path('user/delete', views.del_user, name='deleteProfile'),

]
