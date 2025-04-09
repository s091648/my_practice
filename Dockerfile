# 使用最新的 Python 官方鏡像
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製專案文件
COPY . .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 啟動應用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 