from openai import OpenAI
from app.domain.speech.speech_recognizer import SpeechRecognizer

class OpenAIWhisperRecognizer(SpeechRecognizer):
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    def recognize(self, audio_file_path: str) -> str:
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return response.text
        except Exception as e:
            print(f"語音辨識失敗: {str(e)}")
            raise 