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
    path('login', views.contacts, name='Login'),
    path('new_user', views.contacts, name='SignUp'),
    path('profile', views.contacts, name='Profile'),
    path('user', views.contacts, name='UserPage'),
    path('user/list', views.contacts, name='UserList'),
    path('user/profit', views.contacts, name='Profit'),
    path('contacts', views.contacts, name='Contacts'),
    path('user/delete', views.contacts, name='deleteProfile'),

]
