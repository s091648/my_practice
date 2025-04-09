#!/bin/bash

# 設定錯誤時立即退出
set -e

echo "開始打包專案..."

# 1. 檢查並刪除已存在的臨時目錄
if [ -d "temp_for_zip" ]; then
    echo "刪除舊的臨時目錄..."
    rm -rf temp_for_zip
fi

# 2. 創建臨時目錄
echo "創建臨時目錄..."
mkdir -p temp_for_zip

# 3. 複製 git 追蹤的文件
echo "複製 git 追蹤的文件..."
git ls-files | while read file; do
    mkdir -p "temp_for_zip/$(dirname "$file")"
    cp "$file" "temp_for_zip/$file"
done

# 4. 複製 .coverage_report 目錄
if [ -d ".coverage_report" ]; then
    echo "複製 .coverage_report 目錄..."
    cp -r .coverage_report temp_for_zip/
fi

# 5. 確保 data 目錄存在並複製 CSV 文件
echo "複製 data/backend_users.csv..."
mkdir -p temp_for_zip/data
cp data/backend_users.csv temp_for_zip/data/

# 6. 創建 zip 檔案
echo "創建 zip 檔案..."
if [ -f "project.zip" ]; then
    rm project.zip
fi

cd temp_for_zip
zip -r ../project.zip .
cd ..

# 7. 清理臨時目錄
echo "清理臨時文件..."
rm -rf temp_for_zip

echo "完成！專案已打包為 project.zip"