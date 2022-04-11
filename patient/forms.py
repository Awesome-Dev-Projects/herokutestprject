from datetime import date, timedelta
import datetime
from django import forms


class CustomDateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    #input_type = "datetime"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class ChooseDateForm(forms.Form):
    date = forms.DateField(widget=CustomDateInput(
        format=["%Y-%m-%d"], attrs={
            'min': datetime.datetime.now().date().strftime("%Y-%m-%d"),
            'max': (datetime.datetime.now() + timedelta(days=7)).date().strftime("%Y-%m-%d"),
        }), label="Select Date", required=True, initial=date.today(), error_messages={
            'required': 'Please select date',
    })
