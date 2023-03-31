from django.conf import settings


SILLY_AUTH_SETTINGS = {
    # General settings
    "SITE_NAME": None,  # str used in templates if provided
    "GET_ALL_USERS": False,  # True for dev only
    "PRINT_WARNINGS": True,  # print warnings to terminal
    "BASE_TEMPLATE": "silly_auth/_base.html",  # if you use the provided views

    # emails settings
    "EMAIL_TERMINAL_PRINT": True,  # print emails to terminal
    "EMAIL_VALID_TIME": 600,  # seconds

    # login / logout
    "ALLOW_LOGIN_ENDPOINT": True,  # activate this endpoint
    "LOGIN_REDIRECT": None,
    "ALLOW_LOGOUT_ENDPOINT": True,  # activate this endpoint

    # account creation
    "ALLOW_CREATE_USER_ENDPOINT": True,  # activate this endpoint
    "ALLOW_EMAIL_CONFIRM_ENDPOINT": True,  # activate this endpoint (hook for email link)
    "EMAIL_SEND_ACCOUNT_CONFIRM_LINK": True,
    "ACCOUNT_CONFIRMED_REDIRECT": None,
    "EMAIL_CONFIRM_ACCOUNT_TEMPLATE":
        "silly_auth/emails/confirm_email.txt",

    # password reset (forgotten password)
    "ALLOW_RESET_PASSWORD_ENDPOINT": True,  # activate this endpoint
    "EMAIL_SEND_PASSWORD_RESET_LINK": True,
    "EMAIL_RESET_PASSWORD_TEMPLATE":
        "silly_auth/emails/request_password_reset.txt",
    #   default frontend are classic django views, you can change it to
    #   your own views and/or templates
    "RESET_PASSWORD_ENDPOINT": "auth/password/reset/",
    "RESET_PASSWORD_TEMPLATE": "silly_auth/reset_password.html",
    "RESET_PASSWORD_DONE_TEMPLATE": "silly_auth/reset_password_done.html",
    "RESET_PASSWORD_DONE_URL_TO_SITE": None,  # http:// link to site if provided

    # password change
    "ALLOW_CHANGE_PASSWORD_ENDPOINT": True,  # activate this endpoint

}

try:
    for key in settings.SILLY_AUTH:
        SILLY_AUTH_SETTINGS[key] = settings.SILLY_AUTH[key]
except AttributeError:

    pass
