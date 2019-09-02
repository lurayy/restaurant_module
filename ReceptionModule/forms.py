from django import forms
from ApiModule.models import FoodType

class FoodTypeForm(forms.ModelForm):

    class Meta:
        model = FoodType
        fields = ['food_type','description','image']
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length = 32, widget= forms.PasswordInput)

    class Meta: 
        fields = ['username','password']