from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import admin
from django_countries import countries
from phonenumber_field.formfields import PhoneNumberField
from .models import verificationForm,withdraw_request, upgrade

Basic = 'Basic : $300 - $2,999'
Standard = 'Standard : $3,000 - $4,999'
Gold = 'Gold : $5,000 - $8,999'
Bronze = 'Bronze : $9,000 - $14,000'
Platinum = 'Platinum : $15,000 - $20,000'


Account_types = [(Basic,'Basic'), (Standard,'Standard'), (Gold,'Gold'), (Platinum,'Platinum'),]

class signupForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length =50,required =False )
    last_name = forms.CharField(max_length =50,required =False )
    email = forms.EmailField(max_length =200,required =True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':('Phone')}),
        label= ("Phone number"),required=False)
    # phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':('Phone')}),
    #     label= ("Phone number"),required=False)
    country = forms.ChoiceField(choices=list(countries))    

    USD = 'DOLLARS'
    EUR = 'EURO'
    GBP = 'POUNDS'
    pay = [ (EUR,'EURO'),(USD,'dollars'),(GBP,'Pounds'), ]

    # currency = forms.ChoiceField(choices=pay,)
    Account_type = forms.ChoiceField(choices=Account_types,)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country',
            # 'currency',
            'Account_type',
            'password1',
            'password2',
            )

    def save(self, commit = True):
        user = super(signupForm,self).save(commit = False)
        user.country = self.cleaned_data['country']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            return user

class veriForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = verificationForm
        widgets = {
            'confirmed_tag': forms.HiddenInput(),
            'Document_type': forms.EmailInput(attrs={
                'required':True,
                'placeholder':'Enter Document type e.g Passport,Driving Licence e.t.c'
            }),

            }
        fields = ('username','Document_type','document_upload')

class withdraw_request_form(ModelForm):
    class Meta:
        model = withdraw_request
        fields = ('username','amount','wallet_address','Email')


class upgrade_form(ModelForm):
    class Meta:
        model = upgrade
        fields = {
            'Account_type',
        }
        