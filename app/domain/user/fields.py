from enum import Enum

class UserField(str, Enum):
    NAME = "Name"
    AGE = "Age"

OUTPUT_KEYS = [UserField.NAME, UserField.AGE]