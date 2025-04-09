from abc import ABC, abstractmethod
from typing import List
from app.domain.user import User

class IUserDataLoader(ABC):
    @abstractmethod
    def init_users(self, source: str) -> None:
        """Initialize users from given source (could be a file path, URL, etc)."""
        pass

    @abstractmethod
    def load_users(self, source: str) -> List[User]:
        """Load users from given source (could be a file path, URL, etc)."""
        pass
