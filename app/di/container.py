from dependency_injector import containers, providers
from app.infrastructure.repositories.user_repository_csv import UserCSVRepository
from app.infrastructure.services.csv_user_parser import CsvUserParserService
from app.infrastructure.speech.openai_whisper_recognizer import OpenAIWhisperRecognizer
from app.infrastructure.repositories.user_command_operations import UserCommandOperations
from app.use_cases.user.user_use_case import UserUseCase
from app.use_cases.speech.recognize_speech_use_case import RecognizeSpeechUseCase
from app.use_cases.speech.command_understanding_use_case import CommandUnderstandingUseCase
import os
from dotenv import load_dotenv
from app.core.settings import settings

class Container(containers.DeclarativeContainer):
    # 配置
    config = providers.Configuration()
    
    # 基礎設施層（單例）
    user_repository = providers.Singleton(UserCSVRepository)
    csv_parser = providers.Singleton(CsvUserParserService)
    speech_recognizer = providers.Singleton(
        OpenAIWhisperRecognizer,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    command_operations = providers.Singleton(UserCommandOperations)
    
    # 用例層
    user_use_case = providers.Singleton(
        UserUseCase,
        repo=user_repository,
        loader=csv_parser
    )
    
    transcribe_use_case = providers.Factory(
        RecognizeSpeechUseCase,
        recognizer=speech_recognizer
    )
    
    command_understanding_use_case = providers.Factory(
        CommandUnderstandingUseCase,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        command_operations=command_operations
    )

# 創建容器實例
container = Container()

# 初始化 user_use_case
def init_user_use_case():
    # 直接創建 UserUseCase 實例，而不是通過 container
    use_case = UserUseCase(
        repo=container.user_repository(),
        loader=container.csv_parser()
    )
    init_users = use_case.init_users(settings.csv_path)
    use_case.add_multiple_users(init_users)
    return use_case

# 覆蓋原有的 user_use_case provider
container.user_use_case.override(providers.Singleton(init_user_use_case))
