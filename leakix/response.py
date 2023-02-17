from abc import ABCMeta, abstractmethod


class AbstractResponse(metaclass=ABCMeta):
    def __init__(self, response, response_json=None, status_code=None):
        self.response = response
        self._status_code = (
            status_code if status_code is not None else self.response.status_code
        )
        self.response_json = (
            response_json if response_json is not None else response.json()
        )

    def json(self):
        return self.response_json

    def status_code(self):
        return self._status_code

    @abstractmethod
    def is_success(self):
        pass

    @abstractmethod
    def is_error(self):
        pass


class SuccessResponse(AbstractResponse):
    def is_success(self):
        return True

    def is_error(self):
        return False


class ErrorResponse(AbstractResponse):
    def is_success(self):
        return False

    def is_error(self):
        return True


class RateLimitResponse(ErrorResponse):
    pass


class R(AbstractResponse):
    def __init__(self, response, response_json=None, status_code=None):
        super(R, self).__init__(
            response, response_json=response_json, status_code=status_code
        )
