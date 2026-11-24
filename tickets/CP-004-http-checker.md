# CP-004: HTTP Checker

## Goal

Check a configured Service and create a HealthCheck from the result.

## Scope

- Send an HTTP GET request to the Service URL.
- Follow redirects and evaluate the final HTTP response.
- Use a five-second timeout.
- Treat a 2xx response as successful and other HTTP responses as unsuccessful.
- Record a timeout or connection failure as unsuccessful with no status code.
- Create a new HealthCheck for each attempt.
- Leave response time, scheduling, and saved history for later tickets.

## Acceptance Criteria

- A 2xx response creates a successful HealthCheck with the Service ID and status code.
- A non-2xx response creates an unsuccessful HealthCheck with its status code.
- A redirect is followed and evaluated using its final response.
- A timeout or connection failure creates an unsuccessful HealthCheck with no status code.
- Automated tests cover these outcomes without depending on a live website.