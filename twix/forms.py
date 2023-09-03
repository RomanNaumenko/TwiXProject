from django import forms
from .models import Twix


class TwixForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Enter your twix!",
                                   "class": "form-control",
                               }
                           ), label="")

    class Meta:
        model = Twix
        exclude = ("user",)
