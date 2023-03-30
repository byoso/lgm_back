# Django Silly Auth (WIP 50%)

## DRF only

Currently only works with Django Rest Framework, not with classic Django.

## installation

### 01 Install the package

```sh
pip install django-silly-auth
```

### 02 Add the mixin to your user model

Note that you need to have a custom user model created somewhere.

**users/models.py** (or wherever is your user model)
```python
from dango_silly_auth.mixins import SillyAuthUserMixin

class User(SillyAuthUserMixin):
    pass

```

**Just to let you know, you don't actually need to use this except 'confirmed' :**

The mixin adds 2 attributes:

- confirmed : this is the one you need to check whether an account is confirmed or not. Once set to True, it is not expected to be set back to False.
Note that it is different from 'is_active' which is related to some other django behaviors.
- new_email : used by django_silly_auth for email change requests.

and 2 methods:

- get_jwt_token() -> jwt token: used by django_silly_auth
- verify_jwt_token() -> a user object or None: used by django_silly_auth

### 03 Settings and urls

**settings.py**
```python
INSTALLED_APPS = [
    # ...
    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'django_silly_auth',
]

# If used with Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

AUTH_USER_MODEL = '<wherever is your model>.User'

# Optionnal, here the given values are the default ones.
SILLY_AUTH = {
    # use the 'create user' endpoint
    "CREATE_USER": True,
    # use the login endpoint
    "LOGIN": True,
    # use the logout endpoint
    # use the 'get all users' endpoint, for dev, keep it False in production
    "GET_ALL_USERS": False,
    # redirection when login is a success
    "LOGIN_REDIRECT": None, # change it to an url
    # Site name used in emails
    "SITE_NAME": "My great site",
    # send a confirmation email when a new user is created
    "EMAIL_SEND_ACCOUNT_CONFIRM_LINK": True,
    # how long a verification email will remain valid to use
    "EMAIL_VALID_TIME": 600,  # seconds
    # Print the email in the terminal
    "EMAIL_TERMINAL_PRINT": True,
    # you may change the basic templates used in the emails
    "EMAIL_CONFIRM_ACCOUNT_TEMPLATE":
        "silly_auth/emails/confirm_email.txt",
    "EMAIL_RESTE_PASSWORD_TEMPLATE":
        "silly_auth/emails/request_password_reset.txt",
    # After clicking the account confirm link, the account isconfirmed,
    # and then redirected here:
    "ACCOUNT_CONFIRMED_REDIRECT": None, # change it to an url
    # send an email to ask for password change
    "EMAIL_SEND_PASSWORD_CHANGE_LINK": True,
    "CHANGE_PASSWORD_URL": None, # change it to an url
    # display or not the warnings messages
    "PRINT_WARNINGS": True,
}

```
**urls.py**
```python

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django_silly_auth.urls')),
]


```
You're good to go now !

<hr>

## Endpoints
'auth/' (or wherever you included django_silly_auth.urls) +

|Endpoint | method | form-data | Permission | Effects |
|---|---|---|---|---|
| `token/login/` | POST | username, password | | get a jwt token |
| `token/logout/` | GET |  | IsAuthenticated | force delete token |
| `users/` | GET | | | get all users (use only for dev) |
| `confirm_email/<token>/` | GET |  |  | activate from the email link, set user.confirmed to True |

## Autorization with jwt token
For IsAuthenticated permission add this in your headers:

key: Authorization

value: Token {the token}
