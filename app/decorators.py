from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, reverse


def active_users_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.active:
            return function(request, *args, **kwargs)
        return redirect(reverse('index'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap