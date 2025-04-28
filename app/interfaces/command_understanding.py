from abc import ABC, abstractmethod
from typing import Dict, Any

class ICommandUnderstanding(ABC):
    """命令理解器的抽象介面"""
    
    @abstractmethod
    def understand(self, text: str) -> Dict[str, Any]:
        """理解並解析命令文字
        
        Args:
            text: 需要解析的命令文字
            
        Returns:
            解析後的命令結構，包含 action 和 data
        """
        pass 