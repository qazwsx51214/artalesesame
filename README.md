# 🎮 Artale 頻道廣播系統

一個專為 MapleStory Artale 設計的**即時聊天監聽系統**，可以監聽遊戲內公共頻道的聊天內容，並透過現代化的 Web 介面即時顯示。

![系統概覽](https://img.shields.io/badge/Python-3.7+-blue) ![WebSocket](https://img.shields.io/badge/WebSocket-即時推播-green) ![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey)

## ✨ 功能特色

- 🔴 **即時監聽**: 使用 Scapy 監聽 TCP/32800 端口的遊戲封包
- 📡 **WebSocket 推播**: 解析後的聊天內容即時推送給 Web 前端
- 🌐 **現代化介面**: 美觀的 Web 聊天介面，支援響應式設計
- 💾 **歷史訊息**: 自動保存最近 120 分鐘的聊天記錄
- 🎵 **音效通知**: 新訊息時播放提示音效
- 🎨 **多彩顯示**: 完美支援遊戲內的顏色標籤
- 🔍 **關鍵字搜尋**: 即時高亮顯示指定關鍵字
- 🔧 **一鍵啟動**: Windows 批處理腳本，自動檢查環境並啟動

## 📋 系統需求

- **作業系統**: Windows 10/11
- **Python**: 3.7 或更高版本
- **網路權限**: 需要管理員權限（用於封包監聽）
- **遊戲狀態**: MapleStory Artale 必須正在運行

## 🚀 快速開始

### 步驟 1: 下載專案
```bash
# 下載並解壓縮到任意資料夾
# 或使用 git clone
git clone https://github.com/qazwsx51214/artalesame.git
cd artalesame
```

### 步驟 2: 安裝 Python 依賴
```bash
pip install scapy websockets
```

### 步驟 3: 啟動系統

**方法一：一鍵啟動（推薦）**
1. 確保 MapleStory Artale 正在運行
2. **以管理員身份**執行 `啟動系統.bat`
3. 等待系統自動啟動完成

**方法二：手動啟動**
```bash
# 以管理員身份開啟命令提示字元
python main_chat_ws.py
```

### 步驟 4: 開啟 Web 介面
1. 用瀏覽器開啟 `index.html`
2. 或訪問 `http://localhost:8000`（如果啟動了 HTTP 伺服器）

## 📁 檔案說明

| 檔案 | 說明 |
|------|------|
| `main_chat_ws.py` | 🐍 主程式：封包監聽 + WebSocket 伺服器 |
| `index.html` | 🌐 Web 前端：聊天顯示介面 |
| `啟動系統.bat` | ⚡ 一鍵啟動腳本（Windows） |
| `sound.wav` | 🔊 新訊息提示音效 |
| `history_messages.json` | 📚 歷史訊息存檔 |
| `pal-helper/` | 🔧 Chrome 擴充功能輔助工具 |

## 🖥️ 使用教學

### 基本操作
1. **啟動系統後**，您會看到類似以下的輸出：
   ```
   ✅ WebSocket 推播伺服器啟動於 ws://localhost:8765
   >> 🟢 啟動 Sniffer 中（tcp） ✅ 已啟動 MapleStory 聊天 WebSocket 推播器
   ```

2. **開啟 Web 介面**，系統會自動：
   - 連接到 WebSocket 伺服器
   - 載入最近 120 分鐘的歷史訊息
   - 開始即時顯示新的聊天內容

### 進階功能
- **關鍵字高亮**: 在右上角輸入框輸入關鍵字，相關訊息會被高亮顯示
- **頻道篩選**: 點選訊息旁的頻道標籤，可以篩選特定頻道
- **音效控制**: 可以在瀏覽器中調整或關閉音效

## ⚙️ 系統配置

可以在 `main_chat_ws.py` 中修改以下設定：

```python
# 監聽端口（通常不需要修改）
PORT = 32800

# WebSocket 服務端口
WEBSOCKET_PORT = 8765

# 歷史訊息保留時間（分鐘）
BROADCAST_MINUTES = 120
```

## 🔧 故障排除

### 常見問題

**Q: 啟動時顯示「找不到 Python」**
- A: 請安裝 Python 3.7+ 並確保加入系統 PATH

**Q: 提示權限不足**
- A: 必須以**管理員身份**執行程式（封包監聽需要管理員權限）

**Q: 沒有收到任何聊天訊息**
- A: 確認：
  1. MapleStory Artale 正在運行
  2. 遊戲使用預設端口 32800
  3. 程式以管理員權限執行
  4. 防火牆未阻擋程式

**Q: Web 介面無法連接**
- A: 檢查：
  1. 控制台是否顯示 WebSocket 伺服器啟動成功
  2. 端口 8765 是否被其他程式佔用
  3. 瀏覽器是否支援 WebSocket

**Q: 缺少依賴套件**
```bash
pip install scapy websockets
```

### 除錯模式
如需查看詳細的封包內容，可以在 `main_chat_ws.py` 中取消註解：
```python
# 顯示 16 進制內容
print("[封包 16進制內容]")
# ... (取消註解相關行)
```

## 🛡️ 注意事項

### 使用須知
- ⚠️ **需要管理員權限**：封包監聽功能需要管理員權限
- 🔒 **安全考量**：建議在安全的網路環境下使用
- 📜 **合規使用**：請遵守遊戲使用條款和相關法律法規
- 💾 **隱私保護**：歷史訊息檔案可能包含個人對話，請妥善保管

### 效能建議
- 長時間使用時，建議定期重啟程式以釋放記憶體
- 如果聊天量很大，可以適當調整 `BROADCAST_MINUTES` 來減少記憶體使用

## 🤝 貢獻與回饋

如果您遇到問題或有改進建議，歡迎：
- 提交 [Issues](https://github.com/qazwsx51214/artalesame/issues)
- 發送 Pull Request
- 分享使用心得

## 📄 授權條款

本專案僅供**學習和研究用途**，請勿用於商業目的。使用時請遵守：
- MapleStory 遊戲使用條款
- 當地網路安全相關法律法規
- 尊重其他玩家的隱私權

---

**🎯 享受更好的遊戲聊天體驗！**

如果這個工具對您有幫助，歡迎給專案一個 ⭐ Star！ 