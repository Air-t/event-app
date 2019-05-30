from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from .models import Event

DATE_PICKER_WIDGET_FROM = forms.DateTimeInput(attrs={
    'class': 'form-control datetimepicker-input text-muted',
    'data-target': '#datetimepicker1',
    'width': '100px',
    'placeholder': 'Start date',
})
DATE_PICKER_WIDGET_TO = forms.DateTimeInput(attrs={
    'class': 'form-control datetimepicker-input text-muted',
    'data-target': '#datetimepicker1',
    'width': '100px',
    'placeholder': 'End date',
})
DATE_INPUT_FORMATS = ['%d/%m/%Y %H:%M']


class FeedbackForm(forms.Form):
    """Form to handle users feedback"""
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 40,
                                                           'rows': 5,
                                                           'placeholder': 'Your comment.'}), required=True, label='')
    email = forms.EmailField(required=True, label='', help_text="Email field")


class EventForm(forms.ModelForm):
    """Form to create new Exam instance"""
    start_date = forms.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        widget=DATE_PICKER_WIDGET_FROM
    )

    end_date = forms.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        widget=DATE_PICKER_WIDGET_TO
    )

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'city']
        labels = {
            'name': '',
            'city': '',

        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Event name goes here.'),
                                           'error_messages': _('This event already exists.'),
                                           }),
            'city': forms.TextInput(attrs={'placeholder': _('City'),
                                           }),
        }


class EventSearchForm(forms.Form):
    name = forms.CharField(required=False, help_text='Name', label='')
    city = forms.CharField(required=False, help_text='City', label='')
    from_date = forms.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        widget=DATE_PICKER_WIDGET_FROM,
        required=False,
    )

    to_date = forms.DateTimeField(
        input_formats=DATE_INPUT_FORMATS,
        widget=DATE_PICKER_WIDGET_TO,
        required=False,
    )


class BookTicketForm(forms.Form):
    quantity = forms.IntegerField(label='', required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'Qty',
        'min': '1',
    }))

    def __init__(self, max_qty=None, *args, **kwargs):
        super(BookTicketForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['max'] = max_qty
