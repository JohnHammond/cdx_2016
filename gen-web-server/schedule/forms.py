from six.moves.builtins import object
from django import forms
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Occurrence


class SpanForm(forms.ModelForm):
    start = forms.DateTimeField(label=_("start"),
                                widget=forms.SplitDateTimeWidget)
    end = forms.DateTimeField(label=_("end"),
                              widget=forms.SplitDateTimeWidget,
                              help_text=_(u"The end time must be later than start time."))

    def clean(self):
        if 'end' in self.cleaned_data and 'start' in self.cleaned_data:
            if self.cleaned_data['end'] <= self.cleaned_data['start']:
                raise forms.ValidationError(_(u"The end time must be later than start time."))
        return self.cleaned_data


class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    end_recurring_period = forms.DateTimeField(label=_(u"End recurring period"),
                                               help_text=_(u"This date is ignored for one time only events."),
                                               required=False)

    class Meta(object):
        model = Event
        exclude = ('creator', 'created_on', 'calendar')


class OccurrenceForm(SpanForm):
    class Meta(object):
        model = Occurrence
        exclude = ('original_start', 'original_end', 'event', 'cancelled')
