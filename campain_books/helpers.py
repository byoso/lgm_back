import uuid

from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings

from django_silly_auth.utils import dsa_send_mail
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

from .models import PlayerCharacter, Campain


User = get_user_model()


def is_game_master(user, campain):
    """Check if a user is a GM of a campain"""
    return campain.game_master == user


def add_table_guest(table, guest):
    """Add a new guest to all the campains of a table"""
    for campain in table.table_campains.all():
        if not campain.campain_pcs.filter(user=guest).exists():
            print(f"add {guest.username} to {campain.title}")
            pc = PlayerCharacter.objects.create(
                user=guest,
                character_name="< anonymous PC >"
                )
            campain.campain_pcs.add(pc)
            campain.save()


def remove_table_guest(table, guest):
    """Remove a guest from all the campains of a table"""
    print(f"remove {guest.username} from {table.name}")

    for campain in table.table_campains.all():
        print(f"remove {guest.username} from {campain.title}")
        if campain.campain_pcs.filter(user=guest).exists():
            pc = PlayerCharacter.objects.get(user=guest, campain=campain)
            campain.campain_pcs.remove(pc)
            campain.save()
            pc.delete()
    table.guests.remove(guest)


def guests_create_or_not(
        request,
        guests_list=None,
        table=None, message="",
        serializer=None,
        *args, **kwargs
        ):
    """Used on creation and update of a table to create the needed guests"""

    # add needed guests
    for guest_email in guests_list:
        if not User.objects.filter(email=guest_email).exists():
            if "@" not in guest_email or len(guest_email) < 5:
                message += f"Impossible to create this guest: {guest_email}.\n"
                continue
            try:
                password = str(uuid.uuid4())
                guest = User.objects.create_user(
                    email=guest_email,
                    username=f"<{guest_email.replace('@', '-')}>",
                    password=password,
                    )
                jwt_token = guest.get_jwt_token()
                context = {
                    'user': guest,
                    'link': conf['SPA_EMAIL_LOGIN_LINK'] + jwt_token,
                    'password': password,
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
        add_table_guest(table, guest)

    # remove unneeded guests
    for guest in table.guests.all():

        if guest.email not in guests_list:
            remove_table_guest(table, guest)
    # print("message: ", message)
    return serializer.data
