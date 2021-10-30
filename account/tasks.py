from celery import task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .utils import activation_token_generator


@task
def send_email_on_registration(domain, uid):
    user = User.objects.get(id=uid)
    token = activation_token_generator.make_token(user)

    email_body = render_to_string('account/activation.html', context={'domain': domain, 'user': user, 'token': token})

    send_mail(
        'Actiate your account',
        'message',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=email_body
    )
