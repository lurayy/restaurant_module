from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from ApiModule.models import CustomUser, StaffPosition
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length = 32, widget= forms.PasswordInput)

    class Meta: 
        fields = ['username','password']
class UserForm(UserCreationForm,ModelForm):
    position = forms.ModelChoiceField(queryset = StaffPosition.objects.all(), label = None)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['first_name','last_name','email','username','position','is_rmanager','phone_number']


# username = forms.CharField(min_length=3, max_length=30)
#     email = forms.EmailField(required = True)
#     first_name = forms.CharField(required =  True)
#     last_name = forms.CharField(required =True)
