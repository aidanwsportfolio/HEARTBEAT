import unittest

from src.service import Service


class TestService(unittest.TestCase):
    def test_valid_creation(self):
        service = Service("Moodle", "https://moodle.lsu.edu", "http")
        self.assertEqual(service.name, "Moodle")
        self.assertEqual(service.url, "https://moodle.lsu.edu")
        self.assertEqual(service.check_type, "http")

    def test_invalid_name_is_rejected(self):
        for name in ("", "   ", None):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    Service(name, "https://moodle.lsu.edu", "http")

    def test_invalid_url_is_rejected(self):
        for url in ("moodle.lsu.edu", "https://", "   ", "https://bad host", "https://example.org:abc"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    Service("Moodle", url, "http")

    def test_http_url_is_accepted(self):
        service = Service("Moodle", "http://moodle.lsu.edu", "http")
        self.assertEqual(service.url, "http://moodle.lsu.edu")
        for url in ("http://example.com", "https://example.com"):
            with self.subTest(url=url):
                service.url = url
                self.assertEqual(service.url, url)

    def test_unsupported_check_type_is_rejected(self):
        with self.assertRaises(ValueError):
            Service("Moodle", "https://moodle.lsu.edu", "ping")

        service = Service("Moodle", "https://moodle.lsu.edu", "http")

        with self.assertRaises(ValueError):
            service.check_type = "ping"

        self.assertEqual(service.check_type, "http")

    def test_service_ids_are_unique_and_stable(self):
        moodle = Service("Moodle", "https://moodle.lsu.edu", "http")
        library = Service("Library", "https://www.lib.lsu.edu", "http")

        self.assertNotEqual(moodle.id, library.id)

        original_id = moodle.id
        moodle.name = "LSU Moodle"
        moodle.url = "https://example.org"

        self.assertEqual(moodle.id, original_id)

    def test_invalid_updates_preserve_existing_values(self):
        service = Service("Moodle", "https://moodle.lsu.edu", "http")

        with self.assertRaises(ValueError):
            service.name = "   "
        self.assertEqual(service.name, "Moodle")

        with self.assertRaises(ValueError):
            service.url = "https://"
        self.assertEqual(service.url, "https://moodle.lsu.edu")

    def test_id_cannot_be_assigned(self):
        service = Service("Moodle", "https://moodle.lsu.edu", "http")
        original_id = service.id

        with self.assertRaises(AttributeError):
            service.id = "replacement"

        self.assertEqual(service.id, original_id)

if __name__ == "__main__":
    unittest.main()
