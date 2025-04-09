from app.interfaces.user_data_loader import IUserDataLoader
from app.domain.user import User, NewUser, UserField
import pandas as pd
from typing import List
from .exceptions import CSVParserException

class CsvUserParserService(IUserDataLoader):

    REQUIRED_COLUMNS = set(UserField)

    def init_users(self, source: str) -> None:
        df = pd.read_csv(source)
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise CSVParserException(f"Missing required columns: {missing}")

        return [User(**row) for _, row in df.iterrows()]

    def load_users(self, source: str) -> List[NewUser]:
        df = pd.read_csv(source)
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise CSVParserException(f"Missing required columns: {missing}")

        return [NewUser(**row) for _, row in df.iterrows()]
