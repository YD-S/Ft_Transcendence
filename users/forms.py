from users.models import User
from django import forms


class AvatarForm(forms.ModelForm):

    avatar = forms.ImageField(required=False)


