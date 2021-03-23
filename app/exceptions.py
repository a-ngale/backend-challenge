"""Custom exceptions used by the app."""
from typing import Optional


class ValidationError(Exception):
    """Raise a validation error when invalid parameters were provided to endpoint.

    Attributes:
        message: A string describing an error occurred. A field of the response payload.
        status_code: an integer HTTP status code.
        payload: a dict of custom fields that should be included in payload json.
    """
    def __init__(
            self, message: str, status_code: Optional[int] = 400,
            payload: Optional[dict] = None):
        """Inits ValidationError with error details."""
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict:
        """Returns a dict with an error payload."""
        response = self.payload or dict()
        response['message'] = self.message
        return response
