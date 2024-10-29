from django import forms

from users.models import User


class AvatarForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'avatar'
        ]
