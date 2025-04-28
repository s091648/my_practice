from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppBaseException
from app.di.bootstrap import setup_app

app = setup_app()

@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response()
    )
