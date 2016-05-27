from django import forms
from django.db import models

class SignupForm(forms.Form):
    help_text = {
            'last_name': """\"If you set "Personal name" or \""""
                    """"Family name", these will """
                    """be shown instead of the username""",
            'email': """Used to mail you your password, """
                    """should you forget it""",
            'tt1': """If you're human, leave this field empty""",
            'username': """\"Preferrably ASCII, without punctuation and spaces, and lowercase\"""",
    }
    first = forms.CharField(label='First Name',min_length=3)
    last = forms.CharField(label='Last Name',min_length=3)
    username = forms.CharField(label='Username', max_length=30,
            min_length=2, 
            help_text=help_text['username'], )
    password1 = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', max_length=30, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True, help_text=help_text['email'])
    picture = forms.FileField(required=False,help_text='This field is not required')
    turing_test1 = forms.CharField(label='Turing test',
            required=False, max_length=10, help_text=help_text['tt1'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def clean_turing_test1(self):
        tt = self.cleaned_data.get('turing_test1').strip()
        if tt:
            raise forms.ValidationError("You failed the Turing Test")
        return tt

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label='New password', max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat new password', max_length=30, widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, min_length=2)
    secret = forms.CharField(label='Secret', max_length=64, required=False)
