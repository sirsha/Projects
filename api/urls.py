from rest_framework import routers
from .serializers import UserSerializer
from . import views
from django.urls import path,include

router = routers.DefaultRouter()
router.register('api/',views.Use)

urlpatterns=[
    path('',include(router.urls)),

]
