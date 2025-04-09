import pytest
import pandas as pd
from app.domain.user.models.user import User
from app.domain.user.models.new_user import NewUser
from app.infrastructure.repositories.exceptions import DataframeKeyException, GroupbyKeyException
from app.infrastructure.repositories.user_repository_csv import UserCSVRepository
import tempfile
import os

@pytest.fixture
def temp_csv_file():
    # 創建臨時 CSV 文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as f:
        f.write(b"Name,Age\nTest User,25\nAnother User,30")
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def repository(temp_csv_file):
    repo = UserCSVRepository()
    repo.df = pd.read_csv(temp_csv_file)
    repo.df['is_new'] = False  # 添加 is_new 列
    return repo

@pytest.fixture
def sample_users():
    return [
        NewUser(Name="Test User 1", Age=25),
        NewUser(Name="Test User 2", Age=30)
    ]

def test_add_multiple_users(repository):
    # 準備測試數據
    users = [
        NewUser(Name="New User 1", Age=25),
        NewUser(Name="New User 2", Age=30)
    ]
    
    # 執行測試
    repository.add_multiple_users(users)
    
    # 驗證結果
    assert len(repository.df) == 4  # 原有2條記錄 + 新增2條
    assert "New User 1" in repository.df["Name"].values
    assert "New User 2" in repository.df["Name"].values

def test_compute_group_average_basic(repository):
    # 準備測試數據
    groupby = repository.df.groupby("Name")
    
    # 執行測試
    result = repository.compute_group_average(groupby, "Age")
    
    # 驗證結果
    assert isinstance(result, pd.Series)  # 返回值應該是 pandas Series
    assert result["Test User"] == 25
    assert result["Another User"] == 30

def test_compute_group_average_with_invalid_field(repository, sample_users):
    # 準備測試數據
    repository.add_multiple_users(sample_users)
    grouped = repository.get_grouped_users_by('Name')
    
    # 驗證正常情況
    average = repository.compute_group_average(grouped, 'Age')
    assert isinstance(average, pd.Series)
    assert average["Test User 1"] == 25
    assert average["Test User 2"] == 30
    
    # 驗證異常情況
    with pytest.raises(GroupbyKeyException):
        repository.compute_group_average(grouped, 'invalid_field')

def test_create_user(repository):
    # 準備測試數據
    new_user = NewUser(Name="Created User", Age=35)
    
    # 執行測試
    repository.create_user(new_user)
    
    # 驗證結果
    assert len(repository.df) == 3
    assert "Created User" in repository.df["Name"].values
    assert repository.df[repository.df["Name"] == "Created User"]["is_new"].iloc[0] == True

def test_delete_user(repository):
    # 準備測試數據
    user = User(Name="Test User", Age=25)
    initial_len = len(repository.df)
    
    # 執行測試
    repository.delete_user(user)
    
    # 驗證結果
    assert len(repository.df) == initial_len - 1  # 確認記錄被刪除
    assert "Test User" not in repository.df["Name"].values  # 確認特定用戶被刪除

def test_get_added_user(repository):
    # 準備測試數據
    new_user = NewUser(Name="New Added User", Age=40)
    repository.create_user(new_user)
    
    # 執行測試
    added_users = repository.get_added_user()
    
    # 驗證結果
    assert len(added_users) == 1
    assert added_users[0].Name == "New Added User"
    assert added_users[0].Age == 40

def test_get_grouped_users_by_basic(repository):
    # 執行測試
    result = repository.get_grouped_users_by("Name")
    
    # 驗證結果
    assert isinstance(result, pd.core.groupby.generic.DataFrameGroupBy)
    assert len(result.groups) == 2

def test_get_grouped_users_by_with_invalid_field(repository, sample_users):
    # 準備測試數據
    repository.add_multiple_users(sample_users)
    
    # 驗證正常情況
    grouped = repository.get_grouped_users_by('Age')
    assert len(grouped.groups) == 2
    
    # 驗證異常情況
    with pytest.raises(DataframeKeyException):
        repository.get_grouped_users_by('invalid_field')

def test_get_grouped_users_by_first_char_basic(repository):
    # 執行測試
    result = repository.get_grouped_users_by_first_char("Name")
    
    # 驗證結果
    assert isinstance(result, pd.core.groupby.generic.DataFrameGroupBy)
    assert len(result.groups) == 2  # 'T' 和 'A'

def test_get_grouped_users_by_first_char_with_invalid_field(repository, sample_users):
    # 準備測試數據
    repository.add_multiple_users(sample_users)
    
    # 驗證正常情況
    grouped = repository.get_grouped_users_by_first_char('Name')
    assert len(grouped.groups) == 2  # 'T' 和 'A'
    
    # 驗證異常情況
    with pytest.raises(DataframeKeyException):
        repository.get_grouped_users_by_first_char('invalid_field')

def test_has_user(repository):
    # 準備測試數據
    existing_user = User(Name="Test User", Age=25)
    nonexistent_user = User(Name="Nonexistent User", Age=30)
    
    # 執行測試並驗證結果
    assert repository.has_user(existing_user) is True
    assert repository.has_user(nonexistent_user) is False 