from typing import Any
from django import forms
from django.template.defaultfilters import lower, upper

from .models import customer
from django.forms import ValidationError
from django.core.validators import EmailValidator
states_of_india = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamilnadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]
gender_list=["male","female","others"]

class custom(forms.ModelForm):

    class Meta:
        model = customer
        fields ='__all__'
    def clean(self):
        cleaned_data = super().clean()
        data1=self.cleaned_data["Age"]
        email = self.cleaned_data.get('email')
        phonenumber=self.cleaned_data['phonenumber']
        gender=self.cleaned_data['gender']
        state=self.cleaned_data['state']
        p=str(phonenumber)
        ph=len(p)
        if data1 >100:
            raise ValidationError("mention your age properly")
        if email :
            if not (email.endswith('@gmail.com') or not  email.endswith('@sunnetwork.in')):
                raise forms.ValidationError("Email must be from @gmail.com or @sunnetwork.in")

        if ph:
            if ph>10:
                raise forms.ValidationError("number should be lss than 10 digit")
        if state :
            if  not upper(states_of_india) or not lower(states_of_india):
                raise forms.ValidationError("enter proper state of india")
        if gender not in gender_list:
            raise forms.ValidationError("gender should be  male,female or others")
        return cleaned_data
