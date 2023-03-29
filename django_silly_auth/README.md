# Django Silly Auth

## DRF only

Currently only works with Django Rest Framework, not with classic Django.

## installation

### 01 Install the package

```sh
pip install django-silly-auth
```

### 02 Add the mixin to your user model

**users/models.py** (or wherever is your user model)

Note that you need to have a custom user model created somewhere.

You can add 'AbstractUser' before the mixin if you want, otherwise the
mixin alone is an 'AbstractBaseUser'.

```
from dango_silly_auth.mixins import SillyAuthUserMixin

class User(SillyAuthUserMixin):
    pass

```

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

# Optionnal, here are given values are the default ones.
SILLY_AUTH = {
    # use the 'create user' endpoint
    "CREATE_USER": True,
    # use the login endpoint
    "LOGIN": True,
    # use the 'get all users' endpoint, for dev, keep it False in production
    "GET_ALL_USERS": False,
    # redirection when login is a success
    "LOGIN_REDIRECT": None, # change it to an url
    # Site name used in emails
    "SITE_NAME": "My great site",
    # send a confirmation email when a new user is created
    "EMAIL_SEND_ACCOUNT_CONFIRM_LINK": True,
    # After clicking the account confirm link, the account isconfirmed,
    # and then redirected here:
    "ACCOUNT_CONFIRMED_REDIRECT": None, # change it to an url
    # send an email to ask for password change
    "EMAIL_SEND_PASSWORD_CHANGE_LINK": True,
    "PASSWORD_CHANGE_REDIRECT": None, # change it to an url
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

auth/token/login/