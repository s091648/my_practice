from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class CommandOperation:
    name: str
    description: str
    required_fields: List[str]

class ICommandOperations(ABC):
    @abstractmethod
    def get_available_operations(self) -> List[CommandOperation]:
        """獲取所有可用的命令操作"""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """獲取系統提示詞"""
        pass 