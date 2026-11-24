from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from src.health_check import HealthCheck
from src.service import Service


def check_http(service: Service) -> HealthCheck:
    try:
        with urlopen(service.url, timeout=5) as response:
            status_code = response.status
    except HTTPError as exc:
        # urllib raises HTTPError for responses such as 404 and 503.
        # They are still HTTP responses, so retain their status codes.
        status_code = exc.code
    except (URLError, TimeoutError):
        # A connection failure or timeout produced no HTTP response.
        return HealthCheck(service.id, False, None)

    return HealthCheck(service.id, 200 <= status_code <= 299, status_code)