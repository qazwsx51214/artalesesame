chcp 65001
@echo off
title Artale 頻道廣播系統啟動器

echo.
echo ==========================================
echo 🚀 Artale 頻道廣播系統 一鍵啟動器 🚀
echo ==========================================
echo.

cd /d "%~dp0"

rem 檢查 Python 是否可用
echo 🔍 檢查 Python 環境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤：找不到 Python！請確保已安裝 Python 並加入 PATH
    echo 💡 請前往 https://python.org 下載安裝 Python
    pause
    exit /b 1
)

rem 檢查必要檔案是否存在
echo 🔍 檢查程式檔案...
if not exist "main_chat_ws.py" (
    echo ❌ 錯誤：找不到 main_chat_ws.py
    pause
    exit /b 1
)
if not exist "index.html" (
    echo ❌ 錯誤：找不到 index.html
    pause
    exit /b 1
)

echo ✅ 環境檢查完成！
echo.

rem 步驟1: 檢查並清理端口
echo 🔍 步驟1: 檢查端口使用情況...
echo ⏳ 正在檢查端口 8765 和 8000...

rem 檢查並終止佔用端口8765的程序
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8765') do (
    echo 🛑 發現端口8765被PID %%a佔用，正在終止...
    taskkill /f /pid %%a >nul 2>&1
)

rem 檢查並終止佔用端口8000的程序
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo 🛑 發現端口8000被PID %%a佔用，正在終止...
    taskkill /f /pid %%a >nul 2>&1
)

echo ✅ 端口清理完成！
echo.

rem 步驟2: 先啟動網頁伺服器（背景執行）
echo 🌐 步驟2: 啟動網頁伺服器 (http.server)
echo ⏳ 正在背景啟動 HTTP 伺服器於 localhost:8000...
start /b python -m http.server 8000

rem 等待 HTTP 伺服器啟動
timeout /t 3 /nobreak >nul
echo ✅ 網頁伺服器已在背景啟動！
echo.

rem 步驟3: 開啟瀏覽器
echo 🖥️  步驟3: 開啟瀏覽器
echo ⏳ 正在開啟瀏覽器到 http://localhost:8000...
start http://localhost:8000
timeout /t 2 /nobreak >nul
echo ✅ 瀏覽器已開啟！
echo.

echo ==========================================
echo ✅ 基礎系統啟動完成！
echo ==========================================
echo.
echo 📊 系統狀態：
echo   • ✅ HTTP 伺服器：已在背景運行 (localhost:8000)
echo   • ✅ 瀏覽器：已開啟網頁介面
echo   • ⏳ WebSocket 伺服器：準備啟動...
echo.
echo 🛑 停止系統：按 Ctrl+C 然後關閉此視窗
echo.

rem 步驟4: 啟動 WebSocket 伺服器（前景執行，輸出顯示在此窗口）
echo 📡 步驟4: 啟動 WebSocket 伺服器 (main_chat_ws.py)
echo ⏳ 封包監聽和 WebSocket 推播服務即將啟動...
echo 💡 以下將顯示系統運行狀態和封包監聽資訊：
echo.
echo ==========================================
python main_chat_ws.py 