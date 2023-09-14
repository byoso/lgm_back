from rest_framework import permissions
from _adminplus.models import Configuration


class IsSubscriber(permissions.BasePermission):

    def has_permission(self, request, view):
        response = False
        if Configuration.objects.first().active_stripe_subscriptions:
            response = request.user.is_subscriber
        if Configuration.objects.first().active_tip_me:
            response = True
        return response


class IsOwner(permissions.BasePermission):

    message = "You must be the owner of this resource to perform this action."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user in obj.owners.all():
            return True
        return False


class IsGuestOrOwner(permissions.BasePermission):

    message = "You're not allowed to access this resource."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user in obj.owners.all() or user in obj.guests.all():
            return True
        return False
