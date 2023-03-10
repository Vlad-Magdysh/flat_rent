import json
import flask
from http import HTTPStatus
from datetime import datetime, timezone, date

from error import APIError


class CustomJSONResponseEncoder(json.JSONEncoder):
    def __init__(self):
        super().__init__()

    def default(self, o):
        if isinstance(o, datetime):
            return o.replace(tzinfo=timezone.utc).isoformat()
        if isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class ApiResponse:
    def __init__(self, http_status: HTTPStatus, response_payload, message=None):
        self.http_code = http_status.value
        response_message = http_status.phrase if message is None else message
        self._response_payload = {'message': response_message}
        self._response_payload.update(response_payload)

    def generate_response(self, json_encoder=None):
        if json_encoder is None:
            json_encoder = CustomJSONResponseEncoder()
        response = flask.json.jsonify(json.loads(json_encoder.encode(self._response_payload)))
        response.status_code = self.http_code

        return response


class SuccessResponse(ApiResponse):
    def __init__(self, response_payload=None, message=None):
        response_payload = {} if response_payload is None else response_payload
        super().__init__(HTTPStatus.OK, {'data': response_payload}, message=message)


class ErrorResponse(ApiResponse):
    def __init__(self, api_error: APIError):
        super().__init__(api_error.http_status, {'error': api_error.attributes}, message=api_error.message)
