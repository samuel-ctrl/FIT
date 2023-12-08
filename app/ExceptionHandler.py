from typing import Any
from rest_framework.views import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    response = exception_handler(exc, context)
    error_payload = {}
    if response is not None:
        error_payload["status_code"] = response.status_code

        if response.status_code == 401:
            error_payload["details"] = "Authentication Failed."
        else:
            errors = []
            for key, val in response.data.items():
                if isinstance(val, str):
                    errors.append(val)
                elif isinstance(val, list):
                    errors.append(val[0])
            error_payload["details"] = errors

        response.data = error_payload

    return response
