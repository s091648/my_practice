from abc import ABC, abstractmethod

class SpeechRecognizer(ABC):
    @abstractmethod
    def recognize(self, audio_file_path: str) -> str:
        """傳入音訊檔案路徑，回傳辨識出的文字。"""
        pass 