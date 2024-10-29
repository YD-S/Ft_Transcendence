from django import forms

from users.models import User


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['avatar']
