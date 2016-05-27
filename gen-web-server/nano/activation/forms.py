from django import forms

class ActivationForm(forms.Form):
    key = forms.CharField()

