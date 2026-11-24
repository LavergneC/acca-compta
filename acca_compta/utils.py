from django.http import HttpResponseForbidden
from django.utils.log import log_response


def require_htmx(func):
    def wrapper(request, *args, **kwargs):
        if not request.htmx:
            response = HttpResponseForbidden()
            log_response(
                "Not Allowed: this is a HTMX only url",
                response=response,
                request=request,
            )
            return response
        return func(request, *args, **kwargs)

    return wrapper
