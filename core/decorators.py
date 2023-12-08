from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied


def request_user_only(func):
    def wrapper(view, request, *args, **kwargs):
        instance = get_object_or_404(view.model, pk=kwargs.get("pk"))
        if request.user != instance.user:
            raise PermissionDenied("Permission denied")
        return func(view, request, *args, **kwargs)

    return wrapper
