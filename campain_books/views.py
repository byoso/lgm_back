import uuid

from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django_silly_auth.utils import dsa_send_mail
from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf

from .models import Table
from .serializers import TableSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_table(request):
    serializer = TableSerializer(
                    data=request.data,
                    )
    if serializer.is_valid():
        table = serializer.save()
        table.owners.add(request.user)
        message = ""
        for guest_email in request.data.get('guests'):
            if not User.objects.filter(email=guest_email).exists():
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

                # send email for confirmation and invitation notification
            else:
                guest = User.objects.get(email=guest_email)
            table.guests.add(guest)
        return Response(serializer.data)
    raise ValidationError(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_owner(request):
    tables = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tables_as_user(request):
    tables = Table.objects.filter(users=request.user)
    serializer = TableSerializer(tables, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    data = dict()
    tables_as_owner = Table.objects.filter(owners=request.user)
    serializer = TableSerializer(tables_as_owner, many=True)
    data["tables_as_owner"] = serializer.data

    data["additionnal_data"] = "some data"
    return Response(data)
