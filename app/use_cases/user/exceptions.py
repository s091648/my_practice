from app.core.exceptions import AppBaseException

class UserNotFoundError(AppBaseException):
    status_code: int = 404
    detail: str = "User not found."
    exception_type: str = "UserNotFoundError"
