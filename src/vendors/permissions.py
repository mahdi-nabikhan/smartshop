from django.core.exceptions import PermissionDenied
from .models import *


def admin_or_manager_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not (Admin.objects.filter(id=request.user.id).exists() or Managers.objects.filter(id=request.user.id).exists()):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def is_manager(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not Managers.objects.filter(id=request.user.id).exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
