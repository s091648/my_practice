from app.core.exceptions import AppBaseException


class EmptyUserNameError(AppBaseException):
    status_code: int = 422
    detail: str = "User name cannot be empty."
    exception_type: str = "EmptyUserNameError"

class NegativeUserAgeError(AppBaseException):
    status_code: int = 422
    detail: str = "User age cannot be negative."
    exception_type: str = "NegativeUserAgeError"
