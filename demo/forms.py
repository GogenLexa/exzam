from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from demo.models import User


class OrderForm(forms.ModelForm):
    def clean(self):
        super().clean()
        status = self.cleaned_data.get('status')
        rejection_reason = self.cleaned_data.get('rejection_reason')
        if self.instance.status != 'new':
            raise forms.ValidationError({'status': 'должен быть новый'})
        if status == 'canceled' and not rejection_reason:
            raise forms.ValidationError({'rejection_reason': 'должен быть указана'})


def validate_password_len(password):
    if len(password) < 6:
        raise ValidationError('пароль не мение 6 символов')


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-Z0-9-]+$', message='ne ruskie bukvi')],
                               error_messages={
                                   'required': 'обязательное поле',
                                   'unique': 'логин должен быть не обычен'})
    password = forms.CharField(label='Пароль',
                               validators=[validate_password_len],
                               widget=forms.PasswordInput,
                               error_messages={
                                   'required': 'обязательное поле'})
    password2 = forms.CharField(label='Пароль еще раз',
                                validators=[validate_password_len],
                                widget=forms.PasswordInput,
                                error_messages={
                                    'required': 'обязательное поле'})
    email = forms.CharField(label='Почта',
                            error_messages={
                                'required': 'обязательное поле',
                                'invalid': 'почта должен быть верной'})
    name = forms.CharField(label='name',
                           validators=[RegexValidator('^[а-яА-Я-]+$', message=' ruskie bukvi')],
                           error_messages={
                               'required': 'обязательное поле',
                           })
    surname = forms.CharField(label='surname',
                              validators=[RegexValidator('^[а-яА-Я-]+$', message=' ruskie bukvi')],
                              error_messages={
                                  'required': 'обязательное поле'
                              })
    patronymic = forms.CharField(label='patronymic', required=False,
                                 validators=[RegexValidator('^[а-яА-Я-]+$', message=' ruskie bukvi')], )

    rules = forms.BooleanField(label='dadada', initial=True, required=True, error_messages={
        'required': 'обязательное поле',
    })

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'name', 'surname', 'patronymic', 'rules')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('пароли не равны', code='password_mismatch')
            })
