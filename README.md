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

系統定義了多種錯誤類型，所有錯誤都繼承自 `AppBaseException`。每個錯誤都會返回標準化的錯誤響應：

```json
{
    "detail": "ErrorType: 錯誤訊息",
    "status_code": 400,
    "exception_type": "ErrorType"
}
```

### 資料驗證錯誤 (HTTP 400)
- `EmptyUserNameError`
  - 狀態碼：400
  - 訊息："User name cannot be empty."
  - 情境：當使用者名稱為空字串時

- `NegativeUserAgeError`
  - 狀態碼：400
  - 訊息："User age cannot be negative."
  - 情境：當使用者年齡為負數時

### 資源不存在錯誤 (HTTP 404)
- `UserNotFoundError`
  - 狀態碼：404
  - 訊息："User not found."
  - 情境：當要刪除的使用者不存在時

### 資料處理錯誤 (HTTP 400)
- `DataframeKeyException`
  - 狀態碼：400
  - 訊息："Field {field} not found"
  - 情境：當在 DataFrame 操作時找不到指定的欄位

- `GroupbyKeyException`
  - 狀態碼：400
  - 訊息："Field {field} not found in GroupBy"
  - 情境：當在分組操作時找不到指定的欄位

- `CSVParserException`
  - 狀態碼：400
  - 訊息："Missing required columns: {missing}"
  - 情境：當 CSV 檔案缺少必要的欄位時

### 系統錯誤 (HTTP 500)
- `AppBaseException`
  - 狀態碼：500
  - 訊息："Internal server error"
  - 情境：未被捕捉的系統內部錯誤

所有錯誤都會被全局錯誤處理器捕捉，並返回標準化的 JSON 響應。錯誤響應包含：
- HTTP 狀態碼
- 錯誤類型
- 詳細的錯誤訊息

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
