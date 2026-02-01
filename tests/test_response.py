from unittest.mock import Mock

from leakix.response import (
    ErrorResponse,
    RateLimitResponse,
    SuccessResponse,
)


class TestSuccessResponse:
    def test_is_success_returns_true(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}

        response = SuccessResponse(mock_response)

        assert response.is_success() is True
        assert response.is_error() is False

    def test_json_returns_response_json(self):
        mock_response = Mock()
        mock_response.status_code = 200
        expected_json = {"services": [], "leaks": []}
        mock_response.json.return_value = expected_json

        response = SuccessResponse(mock_response)

        assert response.json() == expected_json

    def test_status_code_returns_200(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        response = SuccessResponse(mock_response)

        assert response.status_code() == 200

    def test_custom_response_json(self):
        mock_response = Mock()
        mock_response.status_code = 200
        custom_json = {"custom": "data"}

        response = SuccessResponse(mock_response, response_json=custom_json)

        assert response.json() == custom_json


class TestErrorResponse:
    def test_is_error_returns_true(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "not found"}

        response = ErrorResponse(mock_response)

        assert response.is_error() is True
        assert response.is_success() is False

    def test_status_code_returns_error_code(self):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "internal error"}

        response = ErrorResponse(mock_response)

        assert response.status_code() == 500

    def test_custom_status_code(self):
        mock_response = Mock()
        mock_response.status_code = 204

        response = ErrorResponse(mock_response, response_json=[], status_code=200)

        assert response.status_code() == 200
        assert response.json() == []


class TestRateLimitResponse:
    def test_is_error_returns_true(self):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"reason": "rate-limit"}

        response = RateLimitResponse(mock_response)

        assert response.is_error() is True
        assert response.is_success() is False

    def test_status_code_returns_429(self):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"reason": "rate-limit"}

        response = RateLimitResponse(mock_response)

        assert response.status_code() == 429

    def test_inherits_from_error_response(self):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {}

        response = RateLimitResponse(mock_response)

        assert isinstance(response, ErrorResponse)
