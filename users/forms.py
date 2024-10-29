import logging

from django import forms
from django.contrib.auth import login

from authentication.utils import hash_password
from users.models import User

log = logging.getLogger(__name__)


class UserForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'avatar',
        ]

    def save(self, *args, **kwargs):
        original = self.instance
        user = super().save(commit=False)
        log.debug(self.cleaned_data)
        if "email" in self.changed_data and self.cleaned_data["email"]:
            user.email = original.email
            user.verified_email = False
            user.has_2fa = False
        if "password" in self.changed_data and self.cleaned_data["password"]:
            user.password = hash_password(self.cleaned_data["password"])
        super().save(*args, **kwargs)
