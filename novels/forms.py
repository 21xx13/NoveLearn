from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .models import Reviews, ArticleReviews


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ("text",)


class ArticleReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = ArticleReviews
        fields = ("text",)


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, '', password)
        if commit:
            user.save()
        return user


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Введите E-mail',
        'type': 'email',
        'name': 'email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Новый пароль',
                                          'type': 'password',
                                          'name': 'new_password1'
                                          }),
        strip=False
    )
    new_password2 = forms.CharField(
        label="Ещё раз",
        strip=False,
        help_text="<br>В пароле должно быть минимум 8 символов, только латинские буквы, хотя бы одна цифра, "
                  "могут содержаться спецсимволы: !@#$%^&*",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Ещё раз',
                                          'type': 'password',
                                          'name': 'new_password2'
                                          }),
    )
