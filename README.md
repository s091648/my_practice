# User Management System

這是一個基於 FastAPI 和 Clean Architecture 設計的使用者管理系統。系統採用 CSV 檔案作為資料存儲，實現了基本的使用者管理功能。

> 📝 本文檔由 Cursor AI 協助生成，基於專案的實際架構和程式碼進行分析後產生。

## 專案架構

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

## 功能特點

- 使用者管理 CRUD 操作
- CSV 檔案資料存儲
- 使用者資料驗證
- 批量使用者導入
- 使用者年齡統計分析

## API 端點

- `POST /create_user` - 創建新使用者
- `DELETE /delete_user` - 刪除使用者
- `GET /get_added_user` - 獲取已添加的使用者列表
- `POST /add_multiple_users_from_csv` - 從 CSV 檔案批量導入使用者
- `GET /calc_average_age_of_user_grouped_by_first_char_of_name` - 計算按名字首字母分組的平均年齡

## 安裝與設置

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

## API 文檔

啟動應用後，可以通過以下地址訪問 Swagger UI 文檔：
- http://localhost:8000/docs
- http://localhost:8000/redoc

## 資料格式

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

## 資料驗證規則

- 使用者名稱（Name）：
  - 不能為空
  - 必須提供
- 使用者年齡（Age）：
  - 必須為非負整數
  - 必須提供

## 開發架構

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

## 錯誤處理

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

### 錯誤處理機制

1. **全局異常處理**：
   - 在 `app/main.py` 中註冊全局異常處理器
   - 自動捕獲並格式化所有 `AppBaseException` 異常
   - FastAPI 自動處理 Pydantic 驗證錯誤
   - 確保一致的錯誤響應格式

2. **異常層級**：
   - 核心異常：`AppBaseException`
   - 驗證異常：`EmptyUserNameError`, `NegativeUserAgeError`
   - 業務邏輯異常：`UserNotFoundError`
   - 資料處理異常：`DataframeKeyException`, `GroupbyKeyException`
   - 服務層異常：`CSVParserException`

3. **錯誤響應格式化**：
   - 所有自定義異常都實現 `to_response()` 方法
   - Pydantic 驗證錯誤使用 FastAPI 的標準格式
   - 包含異常類型和詳細訊息

4. **使用方式**：
   ```python
   # 自定義驗證異常
   raise EmptyUserNameError()
   
   # Pydantic 模型驗證
   class User(BaseModel):
       Name: str
       Age: int = Field(ge=0)  # 確保年齡非負
   
   # 自定義訊息的異常
   raise CSVParserException("Missing required columns: Name, Age")
   ```

## 技術堆疊

- FastAPI：現代、快速的 Web 框架
- Pydantic：資料驗證和序列化
- Pandas：CSV 資料處理
- Cursor AI：文檔生成和程式碼分析

## 開發工具

- Cursor IDE：整合 AI 輔助開發功能
- Cursor AI：協助生成文檔和程式碼分析
- Git：版本控制
- Python 3.8+：程式語言環境

## 致謝

特別感謝 Cursor AI 協助生成本文檔，透過對專案結構和程式碼的智能分析，提供了清晰且結構化的文檔內容。

## 測試

專案使用 pytest 進行測試，並使用 pytest-cov 生成覆蓋率報告。

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

測試遵循清晰架構的原則，分為以下幾個主要部分：

1. **基礎設施層測試**：
   - `test_csv_parser.py`：測試 CSV 檔案解析邏輯
     * 驗證 CSV 檔案格式檢查
     * 測試必要欄位驗證
     * 測試資料轉換功能

2. **Repository 層測試** (`test_user_repository.py`)：
   - 測試數據存取邏輯
   - 驗證 CSV 文件操作
   - 確保數據完整性
   - 測試分組和統計功能

3. **Use Case 層測試** (`test_user_use_case.py`)：
   - 測試業務邏輯
   - 驗證錯誤處理
   - 使用 Mock 物件模擬依賴
   - 測試使用者管理相關操作

4. **API 層測試**：
   - `test_user_router.py`：測試 API 端點
     * 驗證請求/響應格式
     * 確保錯誤處理符合 API 規範
     * 測試各種 HTTP 方法
   - `test_main.py`：測試應用程式配置
     * 驗證全局異常處理
     * 測試應用程式啟動配置

5. **測試配置** (`conftest.py`)：
   - 定義共用的測試夾具（Fixtures）
   - 提供測試數據和模擬物件
   - 確保測試環境的一致性

### 覆蓋率報告

覆蓋率報告配置在 `.coveragerc` 文件中，主要特點：
- 排除測試文件和 `__init__.py`
- 包含分支覆蓋率測試
- HTML 格式報告位於 `.coverage_report/html` 目錄
- 提供詳細的覆蓋率統計和未覆蓋程式碼分析

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
