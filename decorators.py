from django.core.exceptions import ImproperlyConfigured

from vending_machine.views.exceptions import RequestBodyNotAcceptable


def require_params(params):
    if not isinstance(params, list):
        raise ImproperlyConfigured

    def decorator(func):
        def func_wrapper(request, *args, **kwargs):
            for param in params:
                if not (request.data.get(param) or request.GET.get(param)):
                    raise RequestBodyNotAcceptable(
                        "{} is required to be passed".format(param)
                    )
            return func(request, *args, **kwargs)

        return func_wrapper

    return decorator
