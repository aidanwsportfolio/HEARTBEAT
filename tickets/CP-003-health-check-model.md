# CP-003: HealthCheck Model

## Goal

Define a HealthCheck record that stores the result of one check of a Service.

## Scope

- Record the stable ID of the Service that was checked.
- Record when the check happened.
- Record whether the check succeeded.
- Record the HTTP status code when a response was received; allow no status code when there was no response.
- Keep each HealthCheck immutable; a later check creates a new record.
- Keep Service configuration in Service and individual observations in HealthCheck.
- Leave response time for a later ticket.

## Success Rule

For the first HTTP checker, a 2xx response is successful. Other HTTP
responses, timeouts, and connection failures are unsuccessful.
CP-004 will perform the HTTP request and create a HealthCheck using this rule.

## Acceptance Criteria

- A HealthCheck references a Service by its stable ID.
- Each record has a timezone-aware timestamp, defaulting to the current UTC time.
- A 2xx status code requires success; other HTTP status codes require failure.
- A failed check may have no status code when no response was received.
- Invalid or inconsistent values are rejected with clear errors.
- An existing HealthCheck cannot be edited.
- Automated tests cover these behaviors.