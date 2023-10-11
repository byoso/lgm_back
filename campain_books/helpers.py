import uuid

from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from django.shortcuts import get_object_or_404

from django_silly_auth.utils import dsa_send_mail
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

from .models import PlayerCharacter

from _adminplus.models import Configuration

User = get_user_model()

def is_subscriber(user):
    """Check if a user is a subscriber"""

    return user.is_subscriber or Configuration.active_tip_me

def is_game_master(user, campain):
    """Check if a user is a GM of a campain"""
    return campain.game_master == user


def is_player(user, pc):
    """Check if a user is the player of a PC"""
    return pc.user == user


def remove_table_guest(table, guest):
    """Remove a guest from all the campains of a table"""
    print(f"remove {guest.username} from {table.name}")

    for campain in table.table_campains.all():
        print(f"remove {guest.username} from {campain.title}")
        if campain.pcs.filter(user=guest).exists():
            pc = get_object_or_404(PlayerCharacter, user=guest, campain=campain)
            campain.pcs.remove(pc)
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
        guest_email = guest_email.strip()
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
                    'link': conf['API_EMAIL_LOGIN_LINK'] + jwt_token,
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
                    'RPGAdventure.eu invitation',
                    msg_text.render(context),
                    settings.EMAIL_HOST_USER,
                    [guest.email],
                    fail_silently=False,
                )

            except Exception as e:
                message += f"Impossible to create this guest: {guest_email}.\n"
                print(e)

        else:
            if request.user.email == guest_email:
                message += "Impossible to invite yourself.\n"
                continue
            guest = get_object_or_404(User, email=guest_email)
        table.guests.add(guest)

    # remove unneeded guests
    for guest in table.guests.all():

        if guest.email not in guests_list:
            remove_table_guest(table, guest)
    return serializer.data


def check_sources_validity(
        user,
        a_type, b_type,
        source_a, source_b,
        a_is_exporting, b_is_exporting
        ):
    """Check if the exchanges are allowed"""
    if a_type == "campain" and source_a.game_master != user:
        return False
    if b_type == "campain" and source_b.game_master != user:
        return False

    if a_type == "collection" and b_type == "collection":
        if source_a.author == user and source_a.author == user:
            return True
        if source_a.author == user and source_b.author != user:
            if a_is_exporting:
                return False
            if b_is_exporting and not source_b.is_copy_free:
                return False
        if source_a.author != user and source_b.author == user:
            if b_is_exporting:
                return False
            if a_is_exporting and not source_a.is_copy_free:
                return False
        if source_a.author != user and source_b.author != user:
            return False

    if a_type == "campain" and b_type == "campain":
        if a_is_exporting and not source_a.is_copy_free:
            if source_b.is_copy_free:
                return False
        if b_is_exporting and not source_b.is_copy_free:
            if source_a.is_copy_free:
                return False

    if a_type == "campain" and b_type == "collection":
        if b_is_exporting and not source_b.is_copy_free:
            if source_b.author != user and source_a.is_copy_free:
                return False
        if a_is_exporting and not source_a.is_copy_free:
            return False

    if a_type == "collection" and b_type == "campain":
        if a_is_exporting and not source_a.is_copy_free:
            if source_a.author != user and source_b.is_copy_free:
                return False
        if b_is_exporting and not source_b.is_copy_free:
            return False

    return True


def check_before_exchanges(user, source_a, source_b, exchanges):
    """Prepares the datas for the real check, returns the result (Bool)"""
    a_type = exchanges['a_type']
    b_type = exchanges['b_type']
    if len(exchanges['from_a']['items']) > 0 or len(exchanges['from_a']['pcs']) > 0:
        a_is_exporting = True
    else:
        a_is_exporting = False
    if len(exchanges['from_b']['items']) > 0 or len(exchanges['from_b']['pcs']) > 0:
        b_is_exporting = True
    else:
        b_is_exporting = False

    # actual validity checking
    return check_sources_validity(
        user,
        a_type, b_type,
        source_a, source_b,
        a_is_exporting, b_is_exporting
        )
