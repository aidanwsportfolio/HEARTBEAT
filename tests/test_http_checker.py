import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from socket import gaierror
from src.http_checker import check_http
from src.service import Service


class TestHttpChecker(unittest.TestCase):
    def setUp(self):
        self.service = Service("Moodle", "https://moodle.lsu.edu", "http")

    @patch("src.http_checker.urlopen")
    def test_successful_response(self, mock_urlopen):
        mock_urlopen.return_value.__enter__.return_value.status = 200

        check = check_http(self.service)

        self.assertEqual(check.service_id, self.service.id)
        self.assertTrue(check.success)
        self.assertEqual(check.status_code, 200)
        mock_urlopen.assert_called_once_with(self.service.url, timeout=5)

    @patch("src.http_checker.urlopen")
    def test_http_error_keeps_status_code(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            self.service.url, 404, "Not Found", {}, None
        )

        check = check_http(self.service)

        self.assertFalse(check.success)
        self.assertEqual(check.status_code, 404)

    @patch("src.http_checker.urlopen")
    def test_dns_failure_has_reason(self, mock_urlopen):
        mock_urlopen.side_effect = URLError(gaierror(-2, "Name not known"))

        check = check_http(self.service)

        self.assertFalse(check.success)
        self.assertIsNone(check.status_code)
        self.assertEqual(check.failure_reason, "DNS error")
    @patch("src.http_checker.urlopen")
    def test_connection_failure_has_no_status_code(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection refused")

        check = check_http(self.service)

        self.assertFalse(check.success)
        self.assertIsNone(check.status_code)

    @patch("src.http_checker.urlopen")
    def test_timeout_has_no_status_code(self, mock_urlopen):
        mock_urlopen.side_effect = TimeoutError("Timed out")

        check = check_http(self.service)

        self.assertFalse(check.success)
        self.assertIsNone(check.status_code)

    def test_redirect_uses_final_response(self):
        class RedirectHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/redirect":
                    self.send_response(302)
                    self.send_header("Location", "/final")
                else:
                    self.send_response(204)
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), RedirectHandler)
        thread = Thread(target=server.serve_forever)
        thread.start()

        try:
            port = server.server_address[1]
            service = Service("Local test", f"http://127.0.0.1:{port}/redirect", "http")

            check = check_http(service)

            self.assertTrue(check.success)
            self.assertEqual(check.status_code, 204)
            self.assertEqual(check.service_id, service.id)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()