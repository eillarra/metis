from allauth.account.forms import SignupForm
from django import forms


class MetisSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
