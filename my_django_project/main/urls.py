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
    path('login', views.login_page, name='Login'),
    path('new_user', views.new_user, name='SignUp'),
    path('profile', views.profile_user, name='Profile'),
    path('user', views.user_page, name='UserPage'),
    path('user/list', views.user_list, name='UserList'),
    path('user/search', views.user_search, name='user_search'),
    path('user/list/search', views.user_search_list, name='user_search_list'),
    path('user/profit', views.user_profit, name='Profit'),
    path('user/list/sel', views.user_list_sel, name='user_list_sel'),
    path('contacts', views.contacts, name='Contacts'),
    path('user/delete', views.del_user, name='deleteProfile'),
    path('user/index', views.logout_user, name='logout_user')
]
