from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from nano.comments import COMMENT_MAX_LENGTH
from nano.comments.models import Comment

class CommentDetailsForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    part_of = forms.CharField(max_length=255, required=False, widget=forms.HiddenInput)
    back_to_url = '' #forms.UrlField()

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = Comment._default_manager.filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            comment = new.comment,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old
                
        return new

class CommentForm(CommentDetailsForm):
    honeypot = forms.CharField(required=False, label=_('If you enter anything in this field your comment will be treated as spam'))

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value
