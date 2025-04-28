from typing import Dict, Any
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.interfaces.command_understanding import ICommandUnderstanding

class CommandUnderstandingUseCase(ICommandUnderstanding):
    def __init__(self, openai_api_key: str):
        load_dotenv()
        self.client = OpenAI(api_key=openai_api_key)

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
                    "content": """你是一個命令解析器，將用戶的語音命令轉換為具體的操作。
                    可用的操作包括：
                    1. 創建用戶 (create_user) - 需要提供 name 和 age
                    2. 刪除用戶 (delete_user) - 需要提供 name 和 age
                    3. 獲取所有用戶 (get_all_users)
                    4. 獲取已添加的用戶 (get_added_user)
                    5. 計算用戶名稱首字母的平均年齡 (calc_average_age)
                    
                    請返回 JSON 格式，例如：
                    {
                        "action": "create_user",
                        "data": {
                            "name": "John",
                            "age": 25
                        }
                    }
                    """
                },
                {"role": "user", "content": f"請解析以下命令並返回 JSON 格式的操作指令：{text}"}
            ]
        )
        
        command_text = response.choices[0].message.content
        return json.loads(command_text) 