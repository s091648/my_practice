import pytest
from unittest.mock import MagicMock
from app.use_cases.user.user_use_case import UserUseCase
from app.domain.user.models.new_user import NewUser
from app.domain.user.models.user import User
from app.use_cases.user.exceptions import UserNotFoundError
from app.interfaces.user_repository import IUserRepository
from app.interfaces.user_data_loader import IUserDataLoader

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

def test_get_user_by_id(user_use_case, mock_repository):
    # 準備測試數據
    expected_user = User(id="1", name="Test User", email="test@example.com", age=25)
    mock_repository.get_by_id.return_value = expected_user
    
    # 執行測試
    user = user_use_case.get_user_by_id("1")
    
    # 驗證結果
    assert user == expected_user
    mock_repository.get_by_id.assert_called_once_with("1")

def test_get_all_users(user_use_case, mock_repository):
    # 準備測試數據
    expected_users = [
        User(id="1", name="User 1", email="user1@example.com", age=25),
        User(id="2", name="User 2", email="user2@example.com", age=30)
    ]
    mock_repository.get_all.return_value = expected_users
    
    # 執行測試
    users = user_use_case.get_all_users()
    
    # 驗證結果
    assert users == expected_users
    mock_repository.get_all.assert_called_once()

def test_create_user(user_use_case, mock_repository):
    # 準備測試數據
    new_user = NewUser(name="New User", email="new@example.com", age=35)
    
    # 執行測試
    user_use_case.create_user(new_user)
    
    # 驗證結果
    mock_repository.create_user.assert_called_once_with(new_user)

def test_delete_user(user_use_case, mock_repository):
    # 準備測試數據
    user = User(id="1", name="Test User", email="test@example.com", age=25)
    mock_repository.has_user.return_value = True
    
    # 執行測試
    user_use_case.delete_user(user)
    
    # 驗證結果
    mock_repository.delete_user.assert_called_once_with(user)

def test_delete_nonexistent_user(user_use_case, mock_repository):
    # 準備測試數據
    user = User(id="1", name="Test User", email="test@example.com", age=25)
    mock_repository.has_user.return_value = False
    
    # 執行測試並驗證異常
    with pytest.raises(UserNotFoundError):
        user_use_case.delete_user(user) 