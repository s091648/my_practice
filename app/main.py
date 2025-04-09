from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppBaseException
from app.api.v1 import user_router

app = FastAPI()
app.include_router(user_router.router)

@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response()
    )
