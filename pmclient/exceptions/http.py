class HttpException(Exception):
    pass

class HttpRequestError(HttpException):
    def __init__(self, response, message=None):
        self.__code = response.status_code
        self.__reason = response.reason
        self.__message = message

    @property
    def code(self):
        return self.__code

    @property
    def reason(self):
        return self.__reason

    @property
    def message(self):
        return self.__message

