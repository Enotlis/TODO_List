from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, User


class RegisterUserForm(forms.ModelForm):
    '''Форма для регистрации пользователя'''
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput,
                                help_text="Введите пароль повторно")

    class Meta:
        model = User
        fields = [
            'username',
            'telegram_acc'
        ]

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise ValidationError("Введеные пароли не совпадают")
        return password2 

    def clean_telegram_acc(self):
        telegram_acc = self.cleaned_data['telegram_acc']
        if telegram_acc !=  '':
            if 'https:////t.me//' in telegram_acc:
                telegram_acc = telegram_acc.replace('https:////t.me//', '')
            elif telegram_acc[0] == '@':
                telegram_acc = telegram_acc[1:]
        return telegram_acc

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            placeholder = self.fields[field].label
            self.fields[field].widget.attrs.update(
                {'class': 'form-control',
                 'placeholder': placeholder}
                )


class LoginUserForm(AuthenticationForm):
    '''Форма для входа пользователя'''
    username = forms.CharField(max_length=100, label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            placeholder = self.fields[field].label
            self.fields[field].widget.attrs.update(
                {'class': 'form-control',
                 'placeholder': placeholder}
                )


class TaskForm(forms.ModelForm):
    '''Форма для задания'''

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            placeholder = self.fields[field].label
            self.fields[field].widget.attrs.update(
                {'class': 'form-control',
                 'placeholder': placeholder}
                )
