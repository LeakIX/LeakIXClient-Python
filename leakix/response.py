from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractResponse(metaclass=ABCMeta):
    def __init__(
        self,
        response: Any,
        response_json: Any = None,
        status_code: int | None = None,
    ) -> None:
        self.response = response
        self._status_code = (
            status_code if status_code is not None else self.response.status_code
        )
        self.response_json = (
            response_json if response_json is not None else response.json()
        )

    def json(self) -> Any:
        return self.response_json

    def status_code(self) -> int:
        return self._status_code

    @abstractmethod
    def is_success(self) -> bool:
        pass

    @abstractmethod
    def is_error(self) -> bool:
        pass


class SuccessResponse(AbstractResponse):
    def is_success(self) -> bool:
        return True

    def is_error(self) -> bool:
        return False


class ErrorResponse(AbstractResponse):
    def is_success(self) -> bool:
        return False

    def is_error(self) -> bool:
        return True


class RateLimitResponse(ErrorResponse):
    pass
