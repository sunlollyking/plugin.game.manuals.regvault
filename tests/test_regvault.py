"""What a search makes of a connection that fails partway."""
import http.client
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources"))

from lib import regvault  # noqa: E402


class Response(object):
    def __init__(self, error):
        self._error = error

    def read(self):
        raise self._error

    def __enter__(self):
        return self

    def __exit__(self, *exception):
        return False


class LookupTest(unittest.TestCase):
    def lookup(self, error):
        with mock.patch("urllib.request.urlopen", return_value=Response(error)):
            return regvault.Client(pace=0).lookup("nes", "0" * 32)

    def test_a_dropped_connection_is_unavailable(self):
        with self.assertRaises(regvault.Unavailable):
            self.lookup(http.client.IncompleteRead(b""))

    def test_a_stalled_connection_is_unavailable(self):
        with self.assertRaises(regvault.Unavailable):
            self.lookup(TimeoutError("timed out"))


if __name__ == "__main__":
    unittest.main()
