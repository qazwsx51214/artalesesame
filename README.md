# Artale 公共頻道外接系統

## 📡 功能特色

- 即時監聽 MapleStory 公共頻道聊天訊息
- WebSocket 即時推播到網頁前端
- 關鍵字高亮顯示
- 自動捲動和音效提醒
- 一鍵複製好友標籤

## 🚀 快速部署到 GitHub Pages

### 步驟一：建立 GitHub Repository

1. 登入 GitHub，點擊右上角 "+" → "New repository"
2. Repository name: `artale-channel-broadcast`
3. 選擇 **Public**
4. 點擊 "Create repository"

### 步驟二：上傳檔案

1. 在 repository 頁面點擊 "uploading an existing file"
2. 拖拽 `index.html` 到上傳區域
3. Commit message: `Add index.html`
4. 點擊 "Commit changes"

### 步驟三：啟用 GitHub Pages

1. 點擊 **Settings** 標籤
2. 左側選單找到 **Pages**
3. Source 選擇 "Deploy from a branch"
4. Branch 選擇 "main"，Folder 選擇 "/ (root)"
5. 點擊 "Save"

### 步驟四：設定 WebSocket 伺服器

你的網站網址會是：`https://你的用戶名.github.io/artale-channel-broadcast/`

**重要**：需要修改 `config.js` 中的 WebSocket 連線設定：

```javascript
// 在 config.js 中修改這行：
WS_HOST: window.location.hostname === 'localhost' ? 'localhost' : '你的伺服器IP或網域',

// 改成你的伺服器 IP 或網域，例如：
WS_HOST: window.location.hostname === 'localhost' ? 'localhost' : '192.168.1.100',
```

**注意**：記得也要上傳 `config.js` 檔案到 GitHub！

### 步驟五：啟動 WebSocket 伺服器

在你的電腦上執行：
```bash
python main_chat_ws.py
```

## 🔧 本地測試

1. 啟動 WebSocket 伺服器：
   ```bash
   python main_chat_ws.py
   ```

2. 啟動 HTTP 伺服器：
   ```bash
   python -m http.server 8000
   ```

3. 開啟瀏覽器訪問：`http://localhost:8000/index.html`

## 📋 系統需求

- Python 3.7+
- 需要安裝的套件：
  ```bash
  pip install scapy websockets
  ```

## 🔒 注意事項

- 需要管理員權限執行 main_chat_ws.py（網路封包監聽）
- 確保防火牆允許 8765 埠的 WebSocket 連線
- 如果要讓外網連線，需要設定路由器埠轉發

## 🆘 故障排除

### WebSocket 連線失敗
1. 確認 main_chat_ws.py 是否正在執行
2. 檢查防火牆設定
3. 確認 IP 位址是否正確

### 無法監聽封包
1. 以管理員權限執行
2. 確認 MapleStory 是否正在運行
3. 檢查網路介面設定

## 📞 支援

如有問題請在 GitHub Issues 中回報。