from django import forms
from .models import Icecreams
from django.contrib.auth import get_user_model

class IcecreamsForm(forms.Form):
	name = forms.CharField(required=False, widget=forms.TextInput( attrs={'placeholder': 'Search'}), max_length=30, label="")
	choices = (('hard', "Hard"), ('soft', "Soft"), ('french', "French"))
	radio_kin = forms.ChoiceField(label="",  required=False, widget=forms.RadioSelect, choices=choices)
	price = forms.IntegerField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Price'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def clean_password(self):
        return Clean_Password(self.cleaned_data['password'])





def Clean_Password(password):
    hasChar = False
    hasNum = False
    if len(password) < 8:
        raise forms.ValidationError("Password must be 8 characters long...")
    for c in password:
        print(type(c))
        try:
            print(int(c))
        except:
            print("str")
        if(type(c) == str):
            hasChar = True
    
        try:
            if(int(c) > -1 or int(c) < 10):
                hasNum = True
        except:
            print("Cannot convert to int")
    if(not hasChar or not hasNum):
        raise forms.ValidationError("Must contain letters and numbers")


    # Always return a value to use as the new cleaned data, even if
    # this method didn't change it.
    return password