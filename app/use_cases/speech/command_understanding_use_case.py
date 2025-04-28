from typing import Dict, Any
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.interfaces.command_understanding import ICommandUnderstanding
from app.interfaces.command_operations import ICommandOperations

class CommandUnderstandingUseCase(ICommandUnderstanding):
    def __init__(self, openai_api_key: str, command_operations: ICommandOperations):
        load_dotenv()
        self.client = OpenAI(api_key=openai_api_key)
        self.command_operations = command_operations

    def understand(self, text: str) -> Dict[str, Any]:
        """理解並解析語音命令
        
        Args:
            text: 語音辨識出的文字
            
        Returns:
            解析後的命令結構
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": self.command_operations.get_system_prompt()
                },
                {"role": "user", "content": f"請解析以下命令並返回 JSON 格式的操作指令：{text}"}
            ]
        )
        
        command_text = response.choices[0].message.content
        return json.loads(command_text) 