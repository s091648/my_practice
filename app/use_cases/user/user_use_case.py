from app.interfaces.user_repository import IUserRepository
from app.interfaces.user_data_loader import IUserDataLoader
from app.domain.user import User, NewUser, UserField
from typing import Optional, List
from .exceptions import UserNotFoundError

class UserUseCase:
    """User management business logic.
    
    This class implements the business logic for user management operations.
    It depends on a user repository interface for data persistence.
    """

    def __init__(self, repo: IUserRepository, loader: IUserDataLoader):
        """Initialize with a user repository implementation.
        
        Args:
            repo: An implementation of IUserRepository for data persistence
            loader: An implementation of IUserDataLoader for data loading
        """
        self.repo = repo
        self.loader = loader

    def add_multiple_users(self, users: List[NewUser]) -> None:
        """Add multiple users to the repository.
        
        Args:
            users: List of users to add
        """
        self.repo.add_multiple_users(users)

    def calc_average_age_grouped_by_first_char_of_name(self) -> Optional[float]:
        """Calculate the average age of users grouped by name.
        
        Returns:
            Average age as float, None if no users exist
        """
        group = self.repo.get_grouped_users_by_first_char(UserField.NAME.value)
        return self.repo.compute_group_average(group, UserField.AGE.value)

    def create_user(self, user: NewUser) -> None:
        """Create a new user in the system.
        
        Args:
            user: The user to create
        """
        self.repo.create_user(user)
    
    def delete_user(self, user: User) -> None:
        """Delete an existing user from the system.
        
        Args:
            user: The user to delete
        """
        if not self.repo.has_user(user):
            raise UserNotFoundError()
        self.repo.delete_user(user)
    
    def get_added_user(self) -> List[NewUser]:
        """Get all newly added users.
        
        Returns:
            List of newly added users, empty list if none exists
        """
        return self.repo.get_added_user()
    
    def init_users(self, source: str) -> List[User]:
        """Initialize users in the repository.
        
        Args:
            source: Path to the source file containing user data
        """
        return self.loader.init_users(source)
    
    def load_users_from_csv(self, csv_path: str) -> List[User]:
        """Load users from a CSV file.
        
        Args:
            csv_path: Path to the CSV file containing user data
        """
        return self.loader.load_users(csv_path)
