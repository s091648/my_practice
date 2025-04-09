# User Management System

這是一個基於 FastAPI 和 Clean Architecture 設計的使用者管理系統。系統採用 CSV 檔案作為資料存儲，實現了基本的使用者管理功能。

> 📝 本文檔由 Cursor AI 協助生成，基於專案的實際架構和程式碼進行分析後產生。

## 專案架構
<details open>

專案採用清晰架構（Clean Architecture）設計，目錄結構如下：

```
app/
├── api/            # API 層，處理 HTTP 請求
├── core/           # 核心配置和共用元件
├── domain/         # 領域模型和業務規則
├── infrastructure/ # 基礎設施實作（如 CSV 存儲）
├── interfaces/     # 介面定義
└── use_cases/      # 使用案例實作
tests/              # 測試目錄
├── conftest.py            # Pytest 共用測試夾具
├── test_csv_parser.py     # CSV 解析器測試
├── test_main.py          # 主應用程式測試
├── test_user_repository.py# Repository 層測試
├── test_user_router.py   # API 層測試
├── test_user_use_case.py # Use Case 層測試
└── __init__.py           # Python 包標識檔
```

</details>

## 功能特點
<details open>

- 使用者管理 CRUD 操作
- CSV 檔案資料存儲
- 使用者資料驗證
- 批量使用者導入
- 使用者年齡統計分析

</details>

## API 端點
<details open>

- `POST /create_user` - 創建新使用者
- `DELETE /delete_user` - 刪除使用者
- `GET /get_added_user` - 獲取已添加的使用者列表
- `POST /add_multiple_users_from_csv` - 從 CSV 檔案批量導入使用者
- `GET /calc_average_age_of_user_grouped_by_first_char_of_name` - 計算按名字首字母分組的平均年齡

</details>

## 安裝與設置
<details open>

1. 建立虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行應用：
```bash
uvicorn app.main:app --reload
```

</details>

## API 文檔
<details open>

啟動應用後，可以通過以下地址訪問 Swagger UI 文檔：
- http://localhost:8000/docs
- http://localhost:8000/redoc

</details>

## 資料格式
<details open>

### 使用者模型

```json
{
    "Name": "string",  // 使用者名稱（必填）
    "Age": int        // 使用者年齡（必填，非負數）
}
```

### CSV 檔案格式

CSV 檔案必須包含以下欄位：
- `Name`：使用者名稱
- `Age`：使用者年齡

</details>

## 資料驗證規則
<details open>

- 使用者名稱（Name）：
  - 不能為空
  - 必須提供
- 使用者年齡（Age）：
  - 必須為非負整數
  - 必須提供

</details>

## 開發架構
<details open>

專案採用清晰架構（Clean Architecture）設計原則：

1. **Domain Layer**：
   - 定義核心業務實體和規則
   - 包含使用者模型和驗證邏輯

2. **Use Cases Layer**：
   - 實作業務邏輯
   - 處理使用者管理操作

3. **Interface Layer**：
   - 定義存儲和資料載入介面
   - 確保業務邏輯與實作細節解耦

4. **Infrastructure Layer**：
   - 提供具體實作
   - 包含 CSV 檔案操作邏輯

5. **API Layer**：
   - 處理 HTTP 請求
   - 提供 RESTful API 端點

</details>

## 錯誤處理
<details open>

系統採用統一的錯誤處理機制，所有異常都繼承自 `AppBaseException`。錯誤響應採用標準化的 JSON 格式：

```json
{
    "detail": "ErrorType: 錯誤訊息",
    "status_code": 422,
    "exception_type": "ErrorType"
}
```

### 資料驗證異常 (HTTP 422)
1. **Pydantic 驗證錯誤**：
   - 狀態碼：422
   - 情境：當請求資料不符合模型定義時
   - 範例：
     ```json
     {
       "detail": [
         {
           "type": "int_parsing",
           "loc": ["body", "Age"],
           "msg": "Input should be a valid integer",
           "input": "invalid"
         }
       ]
     }
     ```

2. **自定義驗證錯誤**：
   - `EmptyUserNameError`
     - 狀態碼：422
     - 訊息："User name cannot be empty."
     - 情境：當使用者名稱為空字串時

   - `NegativeUserAgeError`
     - 狀態碼：422
     - 訊息："User age cannot be negative."
     - 情境：當使用者年齡為負數時

### 核心異常
- `AppBaseException`
  - 狀態碼：500
  - 基礎異常類別
  - 用於處理未分類的系統錯誤

### 業務邏輯異常 (HTTP 404)
- `UserNotFoundError`
  - 狀態碼：404
  - 訊息："User not found."
  - 情境：當要操作的使用者不存在時

### 資料處理異常 (HTTP 400)
- `DataframeKeyException`
  - 狀態碼：400
  - 訊息：動態生成（例如："Field {field} not found"）
  - 情境：當在 DataFrame 操作時找不到指定的欄位

- `GroupbyKeyException`
  - 狀態碼：400
  - 訊息：動態生成（例如："Field {field} not found in GroupBy"）
  - 情境：當在分組操作時找不到指定的欄位

- `CSVParserException`
  - 狀態碼：400
  - 訊息：動態生成（例如："Missing required columns"）
  - 情境：當 CSV 檔案格式或內容不符合要求時

</details>

## 技術堆疊
<details open>

- FastAPI：現代、快速的 Web 框架
- Pydantic：資料驗證和序列化
- Pandas：CSV 資料處理
- Cursor AI：文檔生成和程式碼分析

</details>

## Docker 部署
<details open>

本專案提供 Docker 支援，可以輕鬆地在容器環境中運行應用程式。

### 前置需求

- 安裝 [Docker](https://www.docker.com/get-started)

### Docker 映像檔建立

```bash
docker build -t user-management .
```

### 運行容器

```bash
docker run -p 8000:8000 user-management
```

應用程式將在 http://localhost:8000 上運行，您可以通過以下地址訪問：
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### Docker 配置說明

專案使用以下 Docker 配置：

1. **基礎映像檔**：
   - 使用 `python:3.12-slim` 作為基礎映像檔
   - 選擇 slim 版本以減少映像檔大小

2. **檔案排除**：
   使用 `.dockerignore` 排除不必要的檔案：
   - Python 快取檔案（`__pycache__/`, `*.pyc`）
   - 環境相關（`venv/`, `.env`）
   - 測試相關（`.pytest_cache/`, `.coverage`, `htmlcov/`）
   - 版本控制（`.git/`, `.gitignore`）
   - 文檔（`README.md`）

3. **安全性考慮**：
   - 使用官方 Python 映像檔
   - 避免安裝不必要的套件
   - 使用 `--no-cache-dir` 減少映像檔大小

</details>

## 開發工具
<details open>

- Cursor IDE：整合 AI 輔助開發功能
- Cursor AI：協助生成文檔和程式碼分析
- Git：版本控制
- Python 3.12+：程式語言環境

</details>

## 測試
<details open>

專案使用 pytest 進行測試，並使用 pytest-cov 生成覆蓋率報告。

### 當前測試覆蓋率狀況

根據最新的覆蓋率報告（生成於 2025-04-10），專案達到了優秀的測試覆蓋率：

- **總體覆蓋率**：100%
- **已測試語句數**：202
- **未覆蓋語句數**：0

#### 各模組覆蓋率詳情

| 模組 | 語句數 | 覆蓋率 |
|------|--------|--------|
| api/v1/user_router.py | 33 | 100% |
| core/exceptions.py | 6 | 100% |
| core/settings.py | 6 | 100% |
| domain/user/exceptions.py | 9 | 100% |
| domain/user/fields.py | 5 | 100% |
| domain/user/models/new_user.py | 2 | 100% |
| domain/user/models/user.py | 15 | 100% |
| infrastructure/repositories/exceptions.py | 11 | 100% |
| infrastructure/repositories/user_repository_csv.py | 40 | 100% |
| infrastructure/services/csv_user_parser.py | 19 | 100% |
| infrastructure/services/exceptions.py | 6 | 100% |
| interfaces/user_data_loader.py | 4 | 100% |
| interfaces/user_repository.py | 6 | 100% |
| main.py | 9 | 100% |
| use_cases/user/exceptions.py | 5 | 100% |
| use_cases/user/user_use_case.py | 26 | 100% |

這個完美的測試覆蓋率表明：
1. 所有的程式碼路徑都經過測試
2. 沒有未測試的功能點
3. 測試案例完整且全面

### 執行測試

```bash
# 執行所有測試
pytest

# 執行測試並生成覆蓋率報告
pytest --cov=app --cov-report=html tests/

# 執行特定測試檔案
pytest tests/test_user_repository.py -v

# 執行並顯示詳細測試資訊
pytest -v
```

### 測試架構

1. **基礎設施層測試**：
   - `test_csv_parser.py`：測試 CSV 檔案解析邏輯
   - `test_user_repository.py`：測試數據存取邏輯

2. **API 層測試**：
   - `test_user_router.py`：測試 API 端點
   - `test_main.py`：測試應用程式配置

3. **Use Case 層測試**：
   - `test_user_use_case.py`：測試業務邏輯

### 測試最佳實踐

1. **分層測試**：
   - 每個架構層都有對應的測試
   - 確保各層級的獨立性和完整性

2. **測試隔離**：
   - 使用 fixtures 確保測試獨立性
   - Mock 外部依賴避免副作用

3. **錯誤處理測試**：
   - 驗證各種錯誤情況
   - 確保錯誤回應符合規範

4. **資料驗證**：
   - 測試資料格式驗證
   - 確保資料完整性和正確性

</details>

## 致謝
<details open>

特別感謝 Cursor AI 協助生成本文檔，透過對專案結構和程式碼的智能分析，提供了清晰且結構化的文檔內容。

</details>
