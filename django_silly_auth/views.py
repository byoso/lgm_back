from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django_silly_auth.config import SILLY_AUTH_SETTINGS as conf
from django_silly_auth.forms import ResetPasswordForm

User = get_user_model()


def reset_password(request, token):
    user = User.verify_jwt_token(token)
    if not user:
        return HttpResponse('error: invalid token')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('reset_password_done')
        else:
            return render(request, conf["RESET_PASSWORD_TEMPLATE"], {'form': form})

    if user:
        if not user.confirmed:
            user.confirmed = True
            user.save()
        login(request, user)
        context = {
            "user": user,
            "site_name": conf["SITE_NAME"],
            "form": ResetPasswordForm()
        }
        return render(request, conf["RESET_PASSWORD_TEMPLATE"], context)


@login_required
def password_reset_done(request):
    context = {
        "user": request.user,
        "site_name": conf["SITE_NAME"],
        "link": conf["RESET_PASSWORD_DONE_URL_TO_SITE"]
    }
    return render(request, conf["RESET_PASSWORD_DONE_TEMPLATE"], context)
