"""keivproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

#from keivproject.chahana.api.views import LoginView
from .views import CreateUserAPIView, CreateProfileAPIView
from . import views

app_name = 'chahana'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/',views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user_profile/',views.user_profile),
    path('profile/',views.user_profile, name='profile'),
    path('create/',CreateUserAPIView.as_view()),
    path('obtain/', views.authenticate_user, name='obtain'),
    path('createprofile/',CreateProfileAPIView.as_view()),
    path('follow/',views.follow,name='follow'),
    path('followusers/<int:id>/',views.followinguserss,name='followinguserss'),
    path('delete/<int:id>/',views.deleteUsers,name='deleteusers'),
    path('completeDetails/<int:id>/',views.completeUser,name="completeUser"),
    path('create1/<int:id>', views.create1,name='create1'),
    path('wishlist/',views.HomePageView.as_view()),
	path('product/<int:id>',views.productClass.as_view({'get': 'list'})),
    path('following/',views.Foll.as_view()),
    path('search/',views.search,name='search'),
    path('apioffollowfunction/', views.follow)



]
