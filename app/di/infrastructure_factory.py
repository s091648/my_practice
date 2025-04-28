from app.infrastructure.repositories.user_repository_csv import UserCSVRepository
from app.infrastructure.services.csv_user_parser import CsvUserParserService
from app.interfaces.user_repository import IUserRepository
from app.interfaces.user_data_loader import IUserDataLoader
from app.infrastructure.speech.openai_whisper_recognizer import OpenAIWhisperRecognizer
from app.interfaces.speech_recognizer import ISpeechRecognizer
import os
from dotenv import load_dotenv

class InfrastructureFactory:
    @staticmethod
    def create_user_repository() -> IUserRepository:
        """創建用戶倉儲實例"""
        return UserCSVRepository()
    
    @staticmethod
    def create_user_data_loader() -> IUserDataLoader:
        """創建用戶數據加載器實例"""
        return CsvUserParserService()
    
    @staticmethod
    def create_speech_recognizer() -> ISpeechRecognizer:
        """創建語音辨識器實例"""
        load_dotenv()
        return OpenAIWhisperRecognizer(openai_api_key=os.getenv("OPENAI_API_KEY"))
