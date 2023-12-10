from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import BasketItem, CustomUserModel

from .tasks import email_verification


class UserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        email_verification.delay(user.id)
        return user


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ('entrance', 'floor', 'apartment', 'building', 'latitude', 'longitude', 'address')


class BasketItemAddForm(ModelForm):
    class Meta:
        model = BasketItem
        fields = ('product', 'quantity', 'user')
