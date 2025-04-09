import pytest
from unittest.mock import MagicMock
from app.use_cases.user.user_use_case import UserUseCase
from app.domain.user.models.new_user import NewUser
from app.domain.user.models.user import User
from app.use_cases.user.exceptions import UserNotFoundError
from app.interfaces.user_repository import IUserRepository
from app.interfaces.user_data_loader import IUserDataLoader
from app.domain.user import UserField

@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=IUserRepository)
    return repo

@pytest.fixture
def mock_loader():
    loader = MagicMock(spec=IUserDataLoader)
    return loader

@pytest.fixture
def user_use_case(mock_repository, mock_loader):
    return UserUseCase(mock_repository, mock_loader)

def test_add_multiple_users(user_use_case, mock_repository):
    # 準備測試數據
    users = [
        NewUser(Name="User 1", Age=25),
        NewUser(Name="User 2", Age=30)
    ]
    
    # 執行測試
    user_use_case.add_multiple_users(users)
    
    # 驗證結果
    mock_repository.add_multiple_users.assert_called_once_with(users)

def test_calc_average_age_grouped_by_first_char_of_name(user_use_case, mock_repository):
    # 準備測試數據
    mock_repository.get_grouped_users_by_first_char.return_value = {"A": [User(Name="Alice", Age=25), User(Name="Anna", Age=35)]}
    mock_repository.compute_group_average.return_value = 30.0
    
    # 執行測試
    result = user_use_case.calc_average_age_grouped_by_first_char_of_name()
    
    # 驗證結果
    assert result == 30.0
    mock_repository.get_grouped_users_by_first_char.assert_called_once_with(UserField.NAME.value)
    mock_repository.compute_group_average.assert_called_once()

def test_calc_average_age_grouped_by_first_char_of_name_no_users(user_use_case, mock_repository):
    # 準備測試數據
    mock_repository.get_grouped_users_by_first_char.return_value = {}
    mock_repository.compute_group_average.return_value = None
    
    # 執行測試
    result = user_use_case.calc_average_age_grouped_by_first_char_of_name()
    
    # 驗證結果
    assert result is None

def test_init_users(user_use_case, mock_loader):
    # 準備測試數據
    expected_users = [
        User(Name="User 1", Age=25),
        User(Name="User 2", Age=30)
    ]
    mock_loader.init_users.return_value = expected_users
    
    # 執行測試
    users = user_use_case.init_users("test.csv")
    
    # 驗證結果
    assert users == expected_users
    mock_loader.init_users.assert_called_once_with("test.csv")

def test_get_added_users(user_use_case, mock_repository):
    # 準備測試數據
    expected_users = [
        NewUser(Name="Test User", Age=25)
    ]
    mock_repository.get_added_user.return_value = expected_users
    
    # 執行測試
    users = user_use_case.get_added_user()
    
    # 驗證結果
    assert users == expected_users
    mock_repository.get_added_user.assert_called_once()

def test_load_users_from_csv(user_use_case, mock_loader):
    # 準備測試數據
    expected_users = [
        User(Name="User 1", Age=25),
        User(Name="User 2", Age=30)
    ]
    mock_loader.load_users.return_value = expected_users
    
    # 執行測試
    users = user_use_case.load_users_from_csv("test.csv")
    
    # 驗證結果
    assert users == expected_users
    mock_loader.load_users.assert_called_once_with("test.csv")

def test_create_user(user_use_case, mock_repository):
    # 準備測試數據
    new_user = NewUser(Name="New User", Age=35)
    
    # 執行測試
    user_use_case.create_user(new_user)
    
    # 驗證結果
    mock_repository.create_user.assert_called_once_with(new_user)

def test_delete_user(user_use_case, mock_repository):
    # 準備測試數據
    user = User(Name="Test User", Age=25)
    mock_repository.has_user.return_value = True
    
    # 執行測試
    user_use_case.delete_user(user)
    
    # 驗證結果
    mock_repository.delete_user.assert_called_once_with(user)

def test_delete_nonexistent_user(user_use_case, mock_repository):
    # 準備測試數據
    user = User(Name="Test User", Age=25)
    mock_repository.has_user.return_value = False
    
    # 執行測試並驗證異常
    with pytest.raises(UserNotFoundError):
        user_use_case.delete_user(user) 