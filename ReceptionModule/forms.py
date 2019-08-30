from django import forms
from ApiModule.models import FoodType

class FoodTypeForm(forms.ModelForm):

    class Meta:
        model = FoodType
        fields = ['food_type','description','image']
        