from app.core.exceptions import AppBaseException

class CSVParserException(AppBaseException):
    status_code: int = 400
    exception_type: str = "CSVParserException"

    def __init__(self, message: str):
        self.detail = f"{message}"
