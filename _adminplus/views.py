from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Configuration

User = get_user_model()


def create_user(request):
    if not request.user.is_superuser and request.user.is_active:
        return redirect('admin:index')

    if request.method == 'POST':
        print("=== request.post: ", request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_confirmed = request.POST.get('is_confirmed') == 'on'
        is_subscriber = request.POST.get('is_subscriber') == 'on'

        if len(username) < 1:
            messages.add_message(
                request,
                messages.ERROR,
                message="Userame must be at least 1 character long",
                extra_tags="danger")

            return render(request, '_adminplus/create_user.html')
        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_confirmed = is_confirmed
            user.is_subscriber = is_subscriber
            user.save()
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                message=str(e),
                extra_tags="danger")

            return render(request, '_adminplus/create_user.html')

        messages.add_message(
            request,
            messages.SUCCESS,
            message="User created successfully",
            extra_tags="success")

    return render(request, '_adminplus/create_user.html')


def adminplus(request):
    if not request.user.is_superuser or not request.user.is_active:
        return redirect('admin:index')

    if request.method == 'POST':
        print("=== request.POST - open_subscriptions: ", request.POST.get('open_subscriptions'))
        configuration = Configuration.objects.first()
        if request.POST.get('open_subscriptions') == "on":  # checkbox returns "on" or None
            configuration.open_subscriptions = True
        else:
            configuration.open_subscriptions = False
        configuration.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            message="Configuration updated successfully",
            extra_tags="success")

    configuration = Configuration.objects.first()

    script_name = request.META["SCRIPT_NAME"]
    site_url = "/"
    site_url = (
        script_name if site_url == "/" and script_name else site_url
        )
    context = {
        'configuration': configuration,
        'site_url': site_url,
    }

    return render(request, '_adminplus/adminplus.html', context)
