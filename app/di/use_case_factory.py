from app.use_cases.user.user_use_case import UserUseCase
from app.use_cases.speech.recognize_speech_use_case import RecognizeSpeechUseCase
from app.use_cases.speech.command_understanding_use_case import CommandUnderstandingUseCase
from app.di.infrastructure_factory import InfrastructureFactory
from app.core.settings import settings
from app.interfaces.command_understanding import ICommandUnderstanding
import os
from dotenv import load_dotenv

class UseCaseFactory:
    @staticmethod
    def create_user_use_case() -> UserUseCase:
        """創建用戶用例實例"""
        repo = InfrastructureFactory.create_user_repository()
        loader = InfrastructureFactory.create_user_data_loader()
        use_case = UserUseCase(repo, loader)
        init_users = use_case.init_users(settings.csv_path)
        use_case.add_multiple_users(init_users)
        return use_case
    
    @staticmethod
    def create_transcribe_use_case() -> RecognizeSpeechUseCase:
        """創建語音辨識用例實例"""
        recognizer = InfrastructureFactory.create_speech_recognizer()
        return RecognizeSpeechUseCase(recognizer)
    
    @staticmethod
    def create_command_understanding_use_case() -> ICommandUnderstanding:
        """創建命令理解用例實例"""
        load_dotenv()
        return CommandUnderstandingUseCase(openai_api_key=os.getenv("OPENAI_API_KEY"))
