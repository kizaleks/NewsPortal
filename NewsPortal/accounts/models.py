from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")
    template_name = 'registration/signup.html'

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        # Важно!!! Переменная basic_group (ниже), аргумент name='basic' должен соответствовать названию группы в джанге
        basic_group = Group.objects.get(name='users')
        # через атрибут user_set, возвращающий список всех пользователей этой группы, мы добавляем нового пользователя в эту группу
        basic_group.user_set.add(user)
        email_user=User.objects.get(username=user).email
        send_mail(
            subject='http://127.0.0.1:8000/news',
            # имя клиента и дата записи будут в теме для удобства
            message="Позравляю с регистрацией на новостном портале  http://127.0.0.1:8000/news",  # сообщение с кратким описанием проблемы
            auth_user='kizaleks83@yandex.ru',
            from_email='kizaleks83@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[f'{email_user}']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        return user