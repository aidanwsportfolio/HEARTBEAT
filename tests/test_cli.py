import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.cli import run
from src.health_check import HealthCheck


class TestCli(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.config_path = Path(self.temp_dir.name) / "services.json"

    def write_config(self, entries):
        self.config_path.write_text(json.dumps(entries), encoding="utf-8")

    @patch("src.cli.check_http")
    def test_checks_valid_services(self, mock_check):
        self.write_config([
            {"name": "Moodle", "url": "https://example.com", "check_type": "http"},
            {"name": "Library", "url": "http://example.org", "check_type": "http"},
        ])
        mock_check.side_effect = lambda service: HealthCheck(service.id, True, 200)
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_check.call_count, 2)
        self.assertIn("Moodle: CHECK PASSED | HTTP 200", output.getvalue())
        self.assertIn("Library: CHECK PASSED | HTTP 200", output.getvalue())

    @patch("src.cli.check_http")
    def test_skips_invalid_entry_and_continues(self, mock_check):
        self.write_config([
            {"name": "", "url": "https://example.com", "check_type": "http"},
            {"name": "Library", "url": "https://example.org", "check_type": "http"},
        ])
        mock_check.side_effect = lambda service: HealthCheck(service.id, True, 200)
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 1)
        mock_check.assert_called_once()
        self.assertIn("Entry 1 is invalid:", errors.getvalue())
        self.assertIn("Name must be a non-empty string", errors.getvalue())
        self.assertIn("Library: CHECK PASSED | HTTP 200", output.getvalue())

    @patch("src.cli.check_http")
    def test_failed_check_needs_review_and_returns_one(self, mock_check):
        self.write_config([
            {"name": "Moodle", "url": "https://example.com", "check_type": "http"},
        ])
        mock_check.side_effect = lambda service: HealthCheck(service.id, False, 403)
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 1)
        self.assertIn("Moodle: NEEDS REVIEW | HTTP 403", output.getvalue())
        self.assertIn(
            "Request forbidden; availability for users is unknown.",
            output.getvalue(),
        )

    @patch("src.cli.check_http")
    def test_no_response_displays_reason(self, mock_check):
        self.write_config([
            {"name": "Library", "url": "https://example.org", "check_type": "http"},
        ])
        mock_check.side_effect = lambda service: HealthCheck(
            service.id, False, None, failure_reason="timeout"
        )
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 1)
        self.assertIn("Library: NEEDS REVIEW | HTTP -", output.getvalue())
        self.assertIn("Reason: timeout", output.getvalue())

    def test_missing_file_reports_error(self):
        errors = io.StringIO()

        with redirect_stderr(errors):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 2)
        self.assertIn("Could not read", errors.getvalue())

    def test_malformed_json_reports_error(self):
        self.config_path.write_text("{invalid", encoding="utf-8")
        errors = io.StringIO()

        with redirect_stderr(errors):
            exit_code = run(self.config_path)

        self.assertEqual(exit_code, 2)
        self.assertIn("Invalid JSON", errors.getvalue())


if __name__ == "__main__":
    unittest.main()