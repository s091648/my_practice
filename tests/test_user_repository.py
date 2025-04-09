import pytest
import pandas as pd
from app.domain.user.models.user import User
from app.domain.user.models.new_user import NewUser
from app.infrastructure.repositories.exceptions import DataframeKeyException, GroupbyKeyException
from app.infrastructure.repositories.user_repository_csv import UserCSVRepository

@pytest.fixture
def repository():
    return UserCSVRepository()

@pytest.fixture
def sample_users():
    return [
        NewUser(name="Test User 1", email="test1@example.com", age=25),
        NewUser(name="Test User 2", email="test2@example.com", age=30)
    ]

def test_add_multiple_users(repository, sample_users):
    repository.add_multiple_users(sample_users)
    assert len(repository.df) == 2
    assert repository.df.iloc[0]['name'] == "Test User 1"
    assert repository.df.iloc[1]['name'] == "Test User 2"

def test_create_user(repository):
    new_user = NewUser(name="New User", email="new@example.com", age=35)
    repository.create_user(new_user)
    assert len(repository.df) == 1
    assert repository.df.iloc[0]['name'] == "New User"
    assert repository.df.iloc[0]['is_new'] == True

def test_delete_user(repository, sample_users):
    repository.add_multiple_users(sample_users)
    user = User(id="1", name="Test User 1", email="test1@example.com", age=25)
    repository.delete_user(user)
    assert len(repository.df) == 1
    assert repository.df.iloc[0]['name'] == "Test User 2"

def test_get_added_user(repository, sample_users):
    repository.add_multiple_users(sample_users)
    added_users = repository.get_added_user()
    assert len(added_users) == 2
    assert all(isinstance(user, NewUser) for user in added_users)

def test_get_grouped_users_by(repository, sample_users):
    repository.add_multiple_users(sample_users)
    grouped = repository.get_grouped_users_by('age')
    assert len(grouped.groups) == 2
    
    with pytest.raises(DataframeKeyException):
        repository.get_grouped_users_by('invalid_field')

def test_get_grouped_users_by_first_char(repository, sample_users):
    repository.add_multiple_users(sample_users)
    grouped = repository.get_grouped_users_by_first_char('name')
    assert len(grouped.groups) == 1  # Both names start with 'T'
    
    with pytest.raises(DataframeKeyException):
        repository.get_grouped_users_by_first_char('invalid_field')

def test_compute_group_average(repository, sample_users):
    repository.add_multiple_users(sample_users)
    grouped = repository.get_grouped_users_by('name')
    average = repository.compute_group_average(grouped, 'age')
    assert len(average) == 2
    assert average['Test User 1'] == 25
    assert average['Test User 2'] == 30
    
    with pytest.raises(GroupbyKeyException):
        repository.compute_group_average(grouped, 'invalid_field') 