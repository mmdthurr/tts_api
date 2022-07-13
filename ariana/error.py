
class InternalError(BaseException):
    def __init__(self, step, msg):
        self.step = step
        self.msg = msg


def error_wrapper(code: int, errors: list):
    return {
        'code': code,
        'errors': errors
    }
