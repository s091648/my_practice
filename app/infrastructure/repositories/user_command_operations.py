from app.interfaces.command_operations import ICommandOperations, CommandOperation

class UserCommandOperations(ICommandOperations):
    def get_available_operations(self) -> list[CommandOperation]:
        return [
            CommandOperation(
                name="create_user",
                description="創建用戶",
                required_fields=["name", "age"]
            ),
            CommandOperation(
                name="delete_user",
                description="刪除用戶",
                required_fields=["name", "age"]
            ),
            CommandOperation(
                name="get_all_users",
                description="獲取所有用戶",
                required_fields=[]
            ),
            CommandOperation(
                name="get_added_user",
                description="獲取已添加的用戶",
                required_fields=[]
            ),
            CommandOperation(
                name="calc_average_age",
                description="計算用戶名稱首字母的平均年齡",
                required_fields=[]
            )
        ]

    def get_system_prompt(self) -> str:
        operations = self.get_available_operations()
        operations_text = "\n".join([
            f"{i+1}. {op.description} ({op.name}) - " + 
            (f"需要提供 {', '.join(op.required_fields)}" if op.required_fields else "無需提供參數")
            for i, op in enumerate(operations)
        ])
        
        return f"""你是一個命令解析器，將用戶的語音命令轉換為具體的操作。
        可用的操作包括：
        {operations_text}
        
        請返回 JSON 格式，例如：
        {{
            "action": "create_user",
            "data": {{
                "name": "John",
                "age": 25
            }}
        }}
        """ 