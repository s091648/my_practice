import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from app.interfaces.user_repository import IUserRepository
from app.domain.user import User, NewUser, UserField
from typing import List, Union
from .exceptions import DataframeKeyException, GroupbyKeyException

class UserCSVRepository(IUserRepository):

    def __init__(self):
        self.df = pd.DataFrame()

    def add_multiple_users(self, users: List[Union[NewUser, User]]) -> None:
        users_df = pd.DataFrame([
            self._user_to_dict(user) for user in users])
        self.df = pd.concat([self.df, users_df], ignore_index=True)

    def compute_group_average(self,
                              groupby: DataFrameGroupBy,
                              field: str) -> pd.Series:
        if field not in groupby.obj.columns:
            raise GroupbyKeyException(f"Field {field} not found in GroupBy")
        return groupby[field].mean()

    def create_user(self, user: NewUser) -> None:
        self.df = pd.concat([self.df,
                             pd.DataFrame([self._user_to_dict(user)])],
                             ignore_index=True)
    
    def delete_user(self, user: User) -> None:
        self.df = self.df.drop(self._query_user(user).index)
    
    def get_added_user(self) -> List[NewUser]:
        added_users = self.df[self.df['is_new']]
        return [NewUser(**row) for _, row in added_users.iterrows()]
    
    def get_grouped_users_by(self, field: str) -> DataFrameGroupBy:
        if field not in self.df.columns:
            raise DataframeKeyException(f"Field {field} not found")
        return self.df.groupby(field)
    
    def get_grouped_users_by_first_char(self, field: str) -> DataFrameGroupBy:
        if field not in self.df.columns:
            raise DataframeKeyException(f"Field {field} not found in Dataframe")
        return self.df.groupby(self.df[field].str[0])

    def has_user(self, user: User) -> bool:
        query = self._query_user(user)
        return not query.empty

    def _describe_user(self, user: User) -> str:
        return f"{UserField.NAME.value} == '{user.Name}' and {UserField.AGE.value} == {user.Age}"

    def _query_user(self, user: User) -> pd.DataFrame:
        return self.df.query(self._describe_user(user))
    
    def _user_to_dict(self, user: Union[NewUser, User]) -> dict:
        return {'is_new': True if isinstance(user, NewUser) else False,
             **user.model_dump()}
