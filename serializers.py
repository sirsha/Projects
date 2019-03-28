from django.contrib.auth.models import User
from rest_framework import serializers, request

from .models import profile, Product, FollowingUsers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        username=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        user_obj = User(
            username= username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


# class ProfileListSerializer(serializers.ListSerializer):
# 	def get(self,instance,validated_data):
# 		return

# class ProfileDataListSerializer(serializers.ListSerializer):
# 	def get(self,instance,validated_data):
# 		return
#
# class ProfileDataSerializer(serializers.Serializer):
# 	value= serializers.CharField()
#
# 	class Meta:
# 		list_serializer_class= ProfileDataListSerializer

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model=profile
       fields = ['firstname','lastname','birthday','bloodgroup','phonenumber']

       def create(self, validated_data):
           firstname = validated_data['firstname']
           lastname = validated_data['lastname']
           birthday = validated_data['birthday']
           bloodgroup = validated_data['bloodgroup']
           phonenumber = validated_data['phonenumber']
           user_obj = profile(
               firstname=firstname,
               lastname=lastname,
               birthday=birthday,
               bloodgroup=bloodgroup,
               phonenumber=phonenumber,
           )
           user_obj.save()
           return validated_data


class HomeDataListSerializer(serializers.ListSerializer):
	def get(self,instance,validated_data):
		return

class HomeDataSerializer(serializers.Serializer):
	value= serializers.CharField()

	class Meta:
		list_serializer_class= HomeDataListSerializer

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model=Product
		fields=['item_name','img_name','subcat_id']

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