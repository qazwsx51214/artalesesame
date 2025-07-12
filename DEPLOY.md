# 🚀 GitHub Pages 部署指南

## 📋 前置需求

- GitHub 帳號
- Python 3.7+ (用於運行 WebSocket 伺服器)
- 網路連線

## 🔧 步驟一：建立 GitHub Repository

1. **登入 GitHub**
2. 點擊右上角 "+" → "New repository"
3. 填寫資訊：
   - Repository name: `artale-channel-broadcast`
   - Description: `Artale 公共頻道外接系統`
   - 選擇 **Public** (GitHub Pages 免費版需要 Public)
   - 不要勾選 "Add a README file"
4. 點擊 "Create repository"

## 📤 步驟二：上傳檔案

### 方法A：網頁上傳（推薦）

1. 在新建的 repository 頁面，點擊 "uploading an existing file"
2. 將以下檔案拖拽到上傳區域：
   - `index.html`
   - `config.js`
   - `README.md`
3. 在下方填寫：
   - Commit message: `Initial commit - Add web interface`
4. 點擊 "Commit changes"

### 方法B：Git 指令（進階）

```bash
git clone https://github.com/你的用戶名/artale-channel-broadcast.git
cd artale-channel-broadcast
# 複製檔案到這個資料夾
git add .
git commit -m "Initial commit - Add web interface"
git push
```

## 🌐 步驟三：啟用 GitHub Pages

1. 在你的 repository 頁面，點擊 **Settings** 標籤
2. 左側選單找到 **Pages**
3. 在 "Source" 區域：
   - 選擇 "Deploy from a branch"
   - Branch 選擇 "main"
   - Folder 選擇 "/ (root)"
   - 點擊 "Save"
4. 等待 2-5 分鐘，GitHub 會顯示你的網站網址

## ⚙️ 步驟四：設定 WebSocket 連線

### 4.1 修改 config.js

在 GitHub 上編輯 `config.js` 檔案：

1. 點擊 `config.js` 檔案
2. 點擊右上角的鉛筆圖示（Edit）
3. 修改這行：
   ```javascript
   // 改成你的伺服器 IP 或網域
   WS_HOST: window.location.hostname === 'localhost' ? 'localhost' : '你的伺服器IP或網域',
   ```
4. 點擊 "Commit changes"

### 4.2 查詢你的 IP 位址

在命令提示字元輸入：
```bash
ipconfig
```
找到你的 IPv4 位址，例如 `192.168.1.100`

### 4.3 設定路由器埠轉發（讓外網能連）

1. 登入路由器管理介面（通常是 192.168.1.1）
2. 找到 "埠轉發" 或 "Port Forwarding"
3. 新增規則：
   - 外部埠：8765
   - 內部 IP：你的電腦 IP
   - 內部埠：8765
   - 協定：TCP

## 🖥️ 步驟五：啟動 WebSocket 伺服器

在你的電腦上執行：

```bash
# 安裝必要套件
pip install scapy websockets

# 啟動伺服器（需要管理員權限）
python main_chat_ws.py
```

## 🌍 步驟六：測試連線

1. 開啟瀏覽器訪問你的 GitHub Pages 網址
2. 確認左上角顯示 "✅ 已連線到伺服器"
3. 如果顯示錯誤，檢查：
   - main_chat_ws.py 是否正在執行
   - config.js 中的 IP 是否正確
   - 防火牆是否允許 8765 埠

## 🔗 分享給其他人

你的網站網址格式：
```
https://你的用戶名.github.io/artale-channel-broadcast/
```

其他人可以直接用這個網址訪問你的聊天監控系統！

## 🆘 常見問題

### Q: 網站顯示 "❌ 連線錯誤"
A: 確認 main_chat_ws.py 是否正在執行，以及 config.js 中的 IP 是否正確

### Q: 無法監聽封包
A: 以管理員權限執行 main_chat_ws.py

### Q: 外網無法連線
A: 檢查路由器埠轉發設定，或使用 ngrok 等工具

### Q: 網站無法載入
A: 確認 GitHub Pages 已啟用，等待 5-10 分鐘讓設定生效

## 📞 需要協助？

如有問題請在 GitHub Issues 中回報，或參考 README.md 中的故障排除章節。 