import pytest
import io
from app.domain.user import NewUser, User

def test_create_user(client):
    # 準備測試數據
    test_user = {
        "Name": "Test User",
        "Age": 25
    }
    
    # 執行測試
    response = client.post("/create_user", json=test_user)
    
    # 驗證結果
    assert response.status_code == 200

def test_delete_user(client):
    # 準備測試數據
    test_user = {
        "Name": "Test User",
        "Age": 25
    }
    
    # 執行測試
    response = client.request(method="DELETE", url="/delete_user", json=test_user)
    
    # 驗證結果
    assert response.status_code == 200

def test_get_added_user(client):
    # 執行測試
    response = client.get("/get_added_user")
    
    # 驗證結果
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # 如果有數據，驗證數據結構
    if response.json():
        user = response.json()[0]
        assert isinstance(user, dict)
        assert "Name" in user
        assert "Age" in user

def test_add_multiple_users_from_csv(client):
    # 準備測試數據
    csv_content = "Name,Age\nTest User 1,25\nTest User 2,30"
    test_file = io.BytesIO(csv_content.encode())
    
    # 執行測試
    response = client.post(
        "/add_multiple_users_from_csv",
        files={"file": ("test.csv", test_file, "text/csv")}
    )
    
    # 驗證結果
    assert response.status_code == 200

def test_calc_average_age_of_user_grouped_by_first_char_of_name(client):
    # 執行測試
    response = client.get("/calc_average_age_of_user_grouped_by_first_char_of_name")
    
    # 驗證結果
    assert response.status_code == 200
    result = response.json()
    # 驗證返回的是一個字典，其中包含了每個首字母對應的平均年齡
    assert isinstance(result, dict)
    for avg_age in result.values():
        assert isinstance(avg_age, (int, float))

def test_create_user_empty_name(client):
    # 準備測試數據 - 無效的用戶數據
    empty_name_user = {
        "Name": "",
        "Age": 25
    }
    
    # 執行測試
    response = client.post("/create_user", json=empty_name_user)
    
    # 驗證結果
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_user_negative_age(client):
    # 準備測試數據 - 無效的用戶數據
    negative_age_user = {
        "Name": "Test User",
        "Age": -1
    }
    
    # 執行測試
    response = client.post("/create_user", json=negative_age_user)
    
    # 驗證結果
    assert response.status_code == 422
    assert "detail" in response.json()

def test_delete_nonexistent_user(client):
    # 準備測試數據
    nonexistent_user = {
        "Name": "Nonexistent User",
        "Age": 25
    }
    
    # 執行測試
    response = client.request(method="DELETE", url="/delete_user", json=nonexistent_user)
    
    # 驗證結果
    assert response.status_code == 404
    assert "detail" in response.json()

def test_create_user_with_invalid_type(client):
    # 準備測試數據 - 類型錯誤
    invalid_user = {
        "Name": "Test User",
        "Age": "not_a_number"
    }
    
    # 執行測試
    response = client.post("/create_user", json=invalid_user)
    
    # 驗證結果
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_user_with_missing_field(client):
    # 準備測試數據 - 缺少必要欄位
    invalid_user = {
        "Name": "Test User"
    }
    
    # 執行測試
    response = client.post("/create_user", json=invalid_user)
    
    # 驗證結果
    assert response.status_code == 422
    assert "detail" in response.json()