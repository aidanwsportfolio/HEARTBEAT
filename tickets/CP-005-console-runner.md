# CP-005: Console Runner

## Goal

Let an operator check services listed in a JSON file with one terminal command.

## Scope

- Read service names, URLs, and check types from a JSON file.
- Validate each entry by creating a Service.
- Report an invalid entry's number and reason, skip it, and continue.
- Run the HTTP checker for each valid Service.
- Print the service name, result, HTTP status, and check time.
- Report a file-level error if the file cannot be read or parsed.
- Leave saved results and stable IDs across separate runs for a later ticket.

## Acceptance Criteria

- One command checks every valid service in the file.
- An invalid entry does not prevent valid entries from being checked.
- Invalid entries identify their position and validation error.
- Malformed or unreadable files produce a clear error.
- Automated tests cover valid entries, skipped entries, and file errors.
- Invalid entries produce exit code 1 after valid services have been checked.
- An unreadable or malformed file produces exit code 2.