from django import forms

from users.models import User


class UserForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'avatar'
        ]
