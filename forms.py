from django import forms
# from django.contrib.auth import authenticate
# from django.contrib.admin.widgets import AdminDateWidget
from . models import  profile, Wish_list

class UserRegisterForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    # confirm_password = forms.CharField(
    #     required=True,
    #     label='confirm_Password',
    #     max_length=32,
    #     widget=forms.PasswordInput()
    # )

# class UserRegisterForm(forms.ModelForm):
#      password = forms.CharField(widget=forms.PasswordInput)
#      confirm_password = forms.CharField(widget=forms.PasswordInput)
#      class Meta:
#         model=Register
#         fields=('username','email','password','confirm_password')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserProfileForm(forms.ModelForm):

   class Meta:
        model= profile
        fields=('firstname','lastname', 'birthday','bloodgroup','photo','phonenumber')
        widgets={
            'birthday':forms.DateInput(attrs={'class':'form_control'})
        }
class WishListForm(forms.ModelForm):
    class Meta:
        model = Wish_list
        fields = ('item_name','img_name')