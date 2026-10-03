# Design Decisions

## Stable Service identity

HEARTBEAT generates a unique, non-editable id for each Service. A service may be renamed or have its URL updated without changing its id. This lets future health-check records continue to refer to the same service.

## Service configuration and check results

Service stores identity and monitoring configuration. A future HealthCheck records what HEARTBEAT observed during an individual check. Results can change from one check to the next, so separating them allows HEARTBEAT to preserve history.
