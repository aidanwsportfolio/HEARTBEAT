from socket import gaierror
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from src.health_check import HealthCheck
from src.service import Service


def check_http(service: Service) -> HealthCheck:
    try:
        with urlopen(service.url, timeout=5) as response:
            status_code = response.status
    except HTTPError as exc:
        # An HTTP error still has a response status, such as 403 or 404.
        status_code = exc.code
    except (URLError, TimeoutError) as exc:
        underlying_reason = getattr(exc, "reason", None)

        if isinstance(exc, TimeoutError) or isinstance(
            underlying_reason, TimeoutError
        ):
            reason = "timeout"
        elif isinstance(underlying_reason, gaierror):
            reason = "DNS error"
        else:
            reason = "connection error"

        return HealthCheck(service.id, False, None, failure_reason=reason)

    return HealthCheck(service.id, 200 <= status_code <= 299, status_code)