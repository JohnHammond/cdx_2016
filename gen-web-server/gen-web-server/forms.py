from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(required=False,label='Email', min_length=3)

class UserSearchForm(forms.Form):
    lastName = forms.CharField(required=False,label='Last Name')

class ContactUsForm(forms.Form):
    name = forms.CharField(label='Name', min_length=3)
    email = forms.EmailField(label='e-mail', min_length=3)
    message = forms.CharField(label='Message',widget=forms.Textarea)
