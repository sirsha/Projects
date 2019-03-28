from rest_framework import serializers
from django.contrib.auth.models import User
from chahana.models import FollowingUsers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','password']

class FollowingUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowingUsers
        fields = ['following_name','user']


class HomeDataListSer(serializers.ListSerializer):
	def get(self,instance,validated_data):
		return

class FollowingUsersSerializer(serializers.Serializer):
	value= serializers.CharField()

	class Meta:
		list_serializer_class= HomeDataListSer