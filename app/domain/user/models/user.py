from pydantic import BaseModel, field_validator
from ..exceptions import EmptyUserNameError, NegativeUserAgeError

class User(BaseModel):
    """Basic user entity."""
    Name: str
    Age: int

    @field_validator("Name")
    def validate_name(cls, v: str) -> str:
        """
        Validate Name attribute with the following rules:
        - Name is required
        - Name cannot be empty
        """
        if len(v) == 0:
            raise EmptyUserNameError()
        return v
    
    @field_validator("Age")
    def validate_age(cls, v: int) -> int:
        """
        Validate Age attribute with the following rules:
        - Age is required
        - Age cannot be negative
        """
        if v < 0:
            raise NegativeUserAgeError()
        return v 