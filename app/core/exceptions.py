class AppBaseException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"
    exception_type: str = "AppBaseException"

    def to_response(self) -> dict:
        return {"detail": f"{self.exception_type}: {self.detail}"}