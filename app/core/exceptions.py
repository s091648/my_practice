class AppBaseException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"
    exception_type: str = "AppBaseException"

    # TODO: 直接回傳JSON(status_code, detail)
    def to_response(self) -> dict:
        return {"detail": f"{self.exception_type}: {self.detail}"}