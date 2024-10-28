from django import forms

from users.models import User


class AvatarForm(forms.Form):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['avatar']
