"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path 
from .views import *
from cookieapp.admin import custom_admin_site
from cookieapp.views import LoginView ,LogoutView
from main.views import TenentsUser

urlpatterns = [


    path('login/', LoginView.as_view(), name="login"),
    path('admin/', custom_admin_site.urls),
    path('tenant-user/',TenentsUserMainView.as_view()),
    path('main/user-tenent-fetch/',TenentsUser.as_view()),
    path('logout/', LogoutView.as_view(), name="logout"),

    
 

 
]