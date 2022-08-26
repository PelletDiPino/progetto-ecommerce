from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields


class UserCreationCustomForm(UserCreationForm):
    is_vendor = fields.BooleanField(label='I am a vendor', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']