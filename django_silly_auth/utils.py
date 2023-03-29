from django.conf import settings
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages

from smtplib import SMTPServerDisconnected

from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

# email address to send emails from
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
validity_time = conf["EMAIL_VALID_TIME"]
email_confirm_account_template = conf["EMAIL_CONFIRM_ACCOUNT_TEMPLATE"]
email_reset_password_template = conf["EMAIL_RESTE_PASSWORD_TEMPLATE"]
site_name = conf["SITE_NAME"]


def send_password_reset_email(request, user):
    token = user.get_jwt_token(expires_in=validity_time)
    domain = request.build_absolute_uri('/')[:-1]
    link = domain + reverse('reset_password', args=[token])
    context = {
        'user': user,
        'link': link,
        'site_name': site_name
    }

    msg_text = get_template(email_reset_password_template)
    print("from ", EMAIL_HOST_USER)
    print(msg_text.render(context))
    try:
        send_mail(
            'Password reset request',
            msg_text.render(context),
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.add_message(
            request, messages.INFO,
            message=(
                f"Please check your email '{user.email}' to "
                "confirm your account and set your password"
                ),
            extra_tags="info"
        )
        print("email sent !")
    except SMTPServerDisconnected as e:
        messages.add_message(
            request,
            messages.ERROR,
            message=(
                "An error occured while sending the email, "
                "but your account has been created. "
                "Please use login / 'forgot password' "
                "to recieve a new email."
            ),
            extra_tags="danger")
        print("SMTPServerDisconnected: ", e)


def send_confirm_email(request, user):
    token = user.get_jwt_token(expires_in=validity_time)
    domain = request.build_absolute_uri('/')[:-1]
    link = domain + reverse('confirm_email', args=[token])
    context = {
        'user': user,
        'link': link,
        'site_name': site_name,
    }

    msg_text = get_template(email_confirm_account_template)

    print("from ", EMAIL_HOST_USER)
    print(msg_text.render(context))
    send_mail(
        'Confirm your new email',
        msg_text.render(context),
        EMAIL_HOST_USER,
        [user.new_email],
        fail_silently=False,
    )


class Color:
    """
    Color class for terminal output
    """
    end = "\x1b[0m"
    info = "\x1b[0;30;36m"
    success = "\x1b[0;30;32m"
    warning = "\x1b[0;30;33m"
    danger = "\x1b[0;30;31m"
