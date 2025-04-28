from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.di.use_case_factory import UseCaseFactory
from app.api.v1 import user_router, voice_router

def setup_app() -> FastAPI:
    """設置並返回 FastAPI 應用程式實例"""
    app = FastAPI()
    
    # 添加 CORS 中間件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 註冊路由
    app.include_router(user_router.router)
    app.include_router(voice_router.router)
    
    # 初始化用戶數據
    @app.on_event("startup")
    async def startup_event():
        use_case = UseCaseFactory.create_user_use_case()
        init_users = use_case.init_users(settings.csv_path)
        use_case.add_multiple_users(init_users)
    
    return app
