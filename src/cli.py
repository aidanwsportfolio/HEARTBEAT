import argparse
import json
import sys
from pathlib import Path

from src.http_checker import check_http
from src.service import Service


def run(config_path: Path) -> int:
    try:
        with config_path.open(encoding="utf-8") as config_file:
            entries = json.load(config_file)
    except OSError as exc:
        print(f"Could not read {config_path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {config_path}: {exc}", file=sys.stderr)
        return 2

    if not isinstance(entries, list):
        print("Configuration must be a JSON list of services.", file=sys.stderr)
        return 2

    has_invalid_entry = False
    has_failed_check = False

    for position, entry in enumerate(entries, start=1):
        try:
            if not isinstance(entry, dict):
                raise ValueError("Expected an object with name, url, and check_type.")
            service = Service(**entry)
        except (TypeError, ValueError) as exc:
            print(f"Entry {position} is invalid: {exc}", file=sys.stderr)
            has_invalid_entry = True
            continue

        check = check_http(service)
        result = "CHECK PASSED" if check.success else "NEEDS REVIEW"
        if not check.success:
            has_failed_check = True

        status = check.status_code if check.status_code is not None else "-"
        print(
            f"{service.name}: {result} | "
            f"HTTP {status} | "
            f"checked {check.checked_at.isoformat()}"
        )
        if check.failure_reason is not None:
            print(f"  Reason: {check.failure_reason}")
        elif check.status_code == 403:
            print("  Request forbidden; availability for users is unknown.")

    return 1 if has_invalid_entry or has_failed_check else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check services listed in a JSON file.")
    parser.add_argument("config", type=Path, help="Path to the services JSON file")
    args = parser.parse_args()
    return run(args.config)


if __name__ == "__main__":
    raise SystemExit(main())