from django import forms
from user_custom.models import CustomUser


class CustomRegistrationForm(forms.Form):
    phone_number = forms.CharField(validators=[CustomUser.phone_regex], required=False, max_length=15)

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass
