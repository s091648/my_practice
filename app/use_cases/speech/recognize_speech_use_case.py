from app.interfaces.speech_recognizer import ISpeechRecognizer

class RecognizeSpeechUseCase:
    def __init__(self, recognizer: ISpeechRecognizer):
        self.recognizer = recognizer

    def execute(self, audio_path: str) -> str:
        """執行語音辨識
        
        Args:
            audio_path: 音頻文件的路徑
            
        Returns:
            辨識出的文字
        """
        return self.recognizer.recognize(audio_path) 