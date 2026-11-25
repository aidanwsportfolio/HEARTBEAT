from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass(frozen=True)
class HealthCheck:
    service_id: str
    success: bool
    status_code: int | None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    failure_reason: str | None = None

    def __post_init__(self):
        try:
            valid_id = UUID(self.service_id)
        except (ValueError, AttributeError, TypeError) as exc:
            raise ValueError("service_id must be a valid Service ID.") from exc

        if valid_id.hex != self.service_id:
            raise ValueError("service_id must match the Service's ID format.")

        if not isinstance(self.success, bool):
            raise ValueError("success must be True or False.")

        if not isinstance(self.checked_at, datetime):
            raise ValueError("checked_at must be a datetime.")

        if self.checked_at.tzinfo is None or self.checked_at.utcoffset() is None:
            raise ValueError("checked_at must include a timezone.")

        if self.status_code is None:
            if self.success:
                raise ValueError("A check without an HTTP response cannot be successful.")
        else:
            if type(self.status_code) is not int or not 100 <= self.status_code <= 599:
                raise ValueError("status_code must be an HTTP status code from 100 to 599.")

            if self.success != (200 <= self.status_code <= 299):
                raise ValueError("success must match whether the HTTP status code is 2xx.")

        if self.failure_reason is not None:
            if not isinstance(self.failure_reason, str) or not self.failure_reason.strip():
                raise ValueError("failure_reason must be a non-empty string.")
            if self.success or self.status_code is not None:
                raise ValueError(
                    "failure_reason is only for failed checks without an HTTP response."
                )