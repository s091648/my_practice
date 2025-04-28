from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppBaseException
from app.di.container import container
from dotenv import load_dotenv
from app.api.v1 import user_router, voice_router

# 載入環境變數
load_dotenv()

# 創建 FastAPI 應用
app = FastAPI()

# 將容器注入到 FastAPI 應用
app.container = container

# 註冊路由
app.include_router(user_router.router)
app.include_router(voice_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Pegatron Practice API"}

@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response()
    )
