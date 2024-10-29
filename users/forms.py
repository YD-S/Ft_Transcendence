from django import forms
from django.contrib.auth import login

from users.models import User


class UserForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'avatar',
            'email',
            'password',
        ]

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        if "email" in self.changed_data:
            user.verified_email = False
            user.has_2fa = False
        if "password" in self.changed_data:
            user.set_password(self.cleaned_data["password"])
        super().save(*args, **kwargs)
