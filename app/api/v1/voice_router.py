from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
import os
from typing import Dict, Any
from app.use_cases.speech.recognize_speech_use_case import RecognizeSpeechUseCase
from app.use_cases.speech.command_understanding_use_case import CommandUnderstandingUseCase
from app.use_cases.user.user_use_case import UserUseCase
from app.domain.user import NewUser, User
from app.di.use_case_factory import UseCaseFactory
from app.interfaces.command_understanding import ICommandUnderstanding
from app.interfaces.speech_recognizer import ISpeechRecognizer

# 設定路由前綴為 /api/v1
router = APIRouter(prefix="/api/v1", tags=["voice"])

def get_transcribe_use_case() -> RecognizeSpeechUseCase:
    """依賴項函數，提供 TranscribeUseCase 實例"""
    return UseCaseFactory.create_transcribe_use_case()

def get_command_understanding_use_case() -> ICommandUnderstanding:
    """依賴項函數，提供 CommandUnderstandingUseCase 實例"""
    return UseCaseFactory.create_command_understanding_use_case()

def get_user_use_case() -> UserUseCase:
    """依賴項函數，提供 UserUseCase 實例"""
    return UseCaseFactory.create_user_use_case()

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    transcribe_use_case: RecognizeSpeechUseCase = Depends(get_transcribe_use_case)
):
    try:
        # 保存上傳的音頻文件
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 使用語音辨識用例
        text = transcribe_use_case.execute(file_path)
        print(f"語音辨識結果: {text}")
        
        # 刪除臨時文件
        os.remove(file_path)
        
        return {"text": text}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"語音辨識失敗: {str(e)}"}
        )

@router.post("/execute_command")
async def execute_command(
    text: str = Form(...),
    command_understanding_use_case: ICommandUnderstanding = Depends(get_command_understanding_use_case),
    user_use_case: UserUseCase = Depends(get_user_use_case)
):
    try:
        print(f"接收到的命令: {text}")
        
        # 使用命令理解用例
        command = command_understanding_use_case.understand(text)
        print(f"解析後的命令: {command}")
        
        # 根據命令執行相應的操作
        action = command.get("action")
        data = command.get("data", {})
        
        if action == "create_user":
            user = NewUser(name=data.get("name"), age=data.get("age"))
            result = user_use_case.create_user(user)
            return {"action": "create_user", "data": result}
            
        elif action == "delete_user":
            user = User(name=data.get("name"), age=data.get("age"))
            result = user_use_case.delete_user(user)
            return {"action": "delete_user", "data": result}
            
        elif action == "get_all_users":
            all_users = user_use_case.get_all_users()
            result = [user.model_dump() for user in all_users]
            return {"action": "get_all_users", "data": result}
            
        elif action == "get_added_user":
            added_users = user_use_case.get_added_user()
            result = [user.model_dump() for user in added_users]
            return {"action": "get_added_user", "data": result}
            
        elif action == "calc_average_age":
            result = user_use_case.calc_average_age_grouped_by_first_char_of_name()
            return {"action": "calc_average_age", "data": result}
            
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "無法識別的命令",
                    "recognized_text": text
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"執行命令失敗: {str(e)}",
                "recognized_text": text
            }
        ) 