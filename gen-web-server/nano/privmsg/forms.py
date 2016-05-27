from django import forms

from nano.privmsg.models import *

class PMForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PMForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'cols': '80'})
        
    class Meta:
        model = PM
        fields = ('text', 'subject')

