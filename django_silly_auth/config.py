from django.conf import settings


SILLY_AUTH_SETTINGS = {
    "SITE_NAME": "<Silly Auth site name>",
    "GET_ALL_USERS": False,
    "EMAIL_CONFIRM": True,
    "EMAIL_VALID_TIME": 600,  # seconds
    "EMAIL_CONFIRM_ACCOUNT_TEMPLATE":
        "silly_auth/emails/confirm_email.txt",
    "EMAIL_RESTE_PASSWORD_TEMPLATE":
        "silly_auth/emails/request_password_reset.txt",
    "LOGIN_REDIRECT": None,
}


for key in settings.SILLY_AUTH:
    SILLY_AUTH_SETTINGS[key] = settings.SILLY_AUTH[key]
