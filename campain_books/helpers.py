import uuid

from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings

from django_silly_auth.utils import dsa_send_mail
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf


User = get_user_model()


def guests_create_or_not(
        request,
        guests_list=None,
        table=None, message="",
        serializer=None,
        *args, **kwargs
        ):

    table.guests.clear()

    for guest_email in guests_list:
        if not User.objects.filter(email=guest_email).exists():
            if "@" not in guest_email or len(guest_email) < 5:
                message += f"Impossible to create this guest: {guest_email}.\n"
                continue
            try:
                guest = User.objects.create_user(
                    email=guest_email,
                    username="guest-" + str(uuid.uuid4()),
                    password=table.table_password,
                    )
                jwt_token = guest.get_jwt_token()
                context = {
                    'user': guest,
                    'link': conf['SPA_EMAIL_LOGIN_LINK'] + jwt_token,
                    'site_name': conf["SITE_NAME"],
                    'table_host_name': request.user.username,
                    'table_name': table.name,
                }

                msg_text = get_template("campains_books/emails/guest_email.txt")
                if conf["EMAIL_TERMINAL_PRINT"]:
                    print("from ", settings.EMAIL_HOST_USER)
                    print(msg_text.render(context))

                dsa_send_mail(
                    'Password reset request',
                    msg_text.render(context),
                    settings.EMAIL_HOST_USER,
                    [guest.email],
                    fail_silently=False,
                )
            except Exception as e:
                message += f"Impossible to create this guest: {guest_email}.\n"
                print(e)

        else:
            guest = User.objects.get(email=guest_email)
        table.guests.add(guest)
    # print("message: ", message)
    return serializer.data
