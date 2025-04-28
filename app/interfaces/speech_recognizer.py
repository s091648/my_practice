from abc import ABC, abstractmethod

class ISpeechRecognizer(ABC):
    """語音辨識器的抽象介面"""
    
    @abstractmethod
    def recognize(self, audio_path: str) -> str:
        """將音頻文件轉換為文字
        
        Args:
            audio_path: 音頻文件的路徑
            
        Returns:
            辨識出的文字
        """
        pass 