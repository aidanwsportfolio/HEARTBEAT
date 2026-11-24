from uuid import uuid4
from urllib.parse import urlsplit

class Service:
    def __init__(self, name: str, url: str, check_type: str):
        self._id = uuid4().hex
        self.name = name
        self.url = url
        self.check_type = check_type

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def check_type(self) -> str:
        return self._check_type

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @url.setter
    def url(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("URL must be a non-empty string.")
        clean_url = value.strip()
        parts = urlsplit(clean_url)
        if parts.scheme not in ("http", "https") or not parts.hostname or any(character.isspace() for character in parts.hostname):
            raise ValueError("URL must start with 'http://' or 'https://' and include a hostname.")
        try:
            parts.port
        except ValueError as exc:
            raise ValueError("URL port must be a number between 0 and 65535.") from exc
        self._url = clean_url

    @check_type.setter
    def check_type(self, value: str):
        if value != "http":
            raise ValueError("Check type must be 'http'.")
        self._check_type = value
