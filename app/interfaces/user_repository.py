from abc import ABC, abstractmethod
from typing import List
from app.domain.user import User, NewUser
from pandas.core.groupby.generic import DataFrameGroupBy
import pandas as pd

class IUserRepository(ABC):
    """Interface for user data persistence operations.
    
    This interface defines the contract for user data storage operations.
    Implementations can use different storage mechanisms (e.g., CSV, Database).
    """

    @abstractmethod
    def add_multiple_users(self, users: List[NewUser]) -> None:
        """Add multiple users from a CSV file to storage.
        
        Args:
            csv_path: Path to the CSV file containing user data
        """
        pass

    @abstractmethod
    def compute_group_average(self,
                              groupby: DataFrameGroupBy,
                              field: str) -> pd.Series:
        """Compute the average of a field from a groupby object.
        
        Args:
            groupby: A pandas groupby object
            field: The field to compute the average of
        Returns:
            The average of the field as a pandas Series
        """
        pass

    @abstractmethod
    def create_user(self, user: User) -> None:
        """Create a new user in the storage.
        
        Args:
            user: The user to create
        """
        pass

    @abstractmethod
    def delete_user(self, user: User) -> None:
        """Delete an existing user from storage.
        
        Args:
            user: The user to delete
        """
        pass

    @abstractmethod
    def delete_user_by_name(self, name: str) -> None:
        """Delete a user by name.
        
        Args:
            name: The name of the user to delete
        """
        pass

    @abstractmethod
    def get_added_user(self) -> List[NewUser]:
        """Retrieve all newly added users from storage.
        
        Returns:
            List of newly added users, empty list if none exists
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Get all users from the dataframe as User instances.
        
        Returns:
            List of all users
        """
        pass

    @abstractmethod
    def get_grouped_users_by(self, field: str) -> DataFrameGroupBy:
        """Get all users from the dataframe as NewUser instances.
        
        Args:
            field: The field to group by
        Returns:
            Grouped users as pd.api.typing.DataFrameGroupBy
        """
        pass

    @abstractmethod
    def get_grouped_users_by_first_char(self, field: str) -> DataFrameGroupBy:
        """Get all users from the dataframe as NewUser instances.
        
        Args:
            field: The field to group by
        Returns:
            Grouped users as pd.api.typing.DataFrameGroupBy
        """
        pass

    @abstractmethod
    def has_user(self, user: User) -> bool:
        """Check if a user exists in storage.
        
        Args:
            user: The user to check
        Returns:
            True if the user exists, False otherwise
        """
        pass
