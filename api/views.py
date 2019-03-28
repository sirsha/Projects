from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User

class Use(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

