from rest_framework import permissions

class IsSubscriber(permissions.BasePermission):
    """
    Check if the user is an active subscriber
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_subscriber and user.is_active
