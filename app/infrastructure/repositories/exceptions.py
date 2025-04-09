from app.core.exceptions import AppBaseException

class DataframeKeyException(AppBaseException):
    status_code: int = 400
    exception_type: str = "DataframeKeyException"

    def __init__(self, message: str):
        self.detail = f"{message}"

class GroupbyKeyException(AppBaseException):
    status_code: int = 400
    exception_type: str = "GroupbyKeyException"

    def __init__(self, message: str):
        self.detail = f"{message}"
