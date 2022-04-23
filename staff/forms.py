from django.contrib.auth.models import Group, User
from django.forms import ModelForm

from .models import Profile


class RolesForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"