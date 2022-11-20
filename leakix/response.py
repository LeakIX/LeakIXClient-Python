from abc import ABCMeta, abstractmethod


class AbstractResponse(metaclass=ABCMeta):
    def __init__(self, response, response_json=None):
        self.response = response
        self.response_json = response_json or response.json()

    def json(self):
        return self.response_json

    def status_code(self):
        return self.response.status_code

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
    def __init__(self, response, response_json=None):
        super(R, self).__init__(response, response_json=response_json)
