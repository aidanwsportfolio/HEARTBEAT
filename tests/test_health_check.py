import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from src.health_check import HealthCheck
from src.service import Service


class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        self.service = Service("Moodle", "https://moodle.lsu.edu", "http")

    def test_successful_response(self):
        check = HealthCheck(self.service.id, True, 200)

        self.assertEqual(check.service_id, self.service.id)
        self.assertTrue(check.success)
        self.assertEqual(check.status_code, 200)
        self.assertIsNotNone(check.checked_at.tzinfo)

    def test_failure_without_response(self):
        check = HealthCheck(self.service.id, False, None)

        self.assertFalse(check.success)
        self.assertIsNone(check.status_code)

    def test_non_2xx_response_is_unsuccessful(self):
        check = HealthCheck(self.service.id, False, 404)

        self.assertFalse(check.success)
        self.assertEqual(check.status_code, 404)

    def test_inconsistent_result_is_rejected(self):
        for success, status_code in ((True, None), (True, 404), (False, 200)):
            with self.subTest(success=success, status_code=status_code):
                with self.assertRaises(ValueError):
                    HealthCheck(self.service.id, success, status_code)

    def test_record_cannot_be_edited(self):
        check = HealthCheck(self.service.id, True, 200)

        with self.assertRaises(FrozenInstanceError):
            check.success = False

    def test_naive_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            HealthCheck(
                self.service.id,
                True,
                200,
                checked_at=datetime(2026, 11, 24),
            )

    def test_non_datetime_timestamp_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "checked_at must be a datetime"):
            HealthCheck(self.service.id, True, 200, checked_at="yesterday")


if __name__ == "__main__":
    unittest.main()
