# CP-002: Implement Service Model

## Goal

Create the first Python Service model from the design in `docs/DATA_MODEL.md`.

## Scope

- Define `id`, `name`, `url`, and `check_type`.
- Generate a unique, stable `id` within HEARTBEAT. The operator cannot set or edit it.
- Require nonempty `name` and `url`.
- Accept `http://` and `https://` URLs with a valid host.
- Support `http` as the initial `check_type`; reject unsupported values.
- Allow the project operator to update `name`, `url`, and `check_type`, subject to the same validation.
- Keep response time, HTTP status, and check results out of `Service`.

## Acceptance Criteria

- Creating a valid Service produces a unique `id` that stays the same after edits.
- Invalid names, URLs, or check types are rejected with clear errors.
- Both HTTP and HTTPS URLs are accepted when structurally valid.
- Updating editable fields applies validation and does not change `id`.
- Automated tests cover valid creation, invalid input, ID stability, and updates.
