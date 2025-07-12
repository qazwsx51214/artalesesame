// WebSocket 連線設定
const CONFIG = {
  // 本地開發時使用 localhost，部署時改成你的伺服器 IP 或網域
  WS_HOST: window.location.hostname === 'localhost' ? 'localhost' : '你的伺服器IP或網域',
  WS_PORT: 8765,
  
  // 音效設定
  SOUND_ENABLED: true,
  SOUND_FILE: 'C:/Windows/Media/Windows Background.wav',
  
  // 自動捲動預設值
  AUTO_SCROLL: true,
  
  // 關鍵字高亮預設值
  KEYWORD_HIGHLIGHT: true
};

// 匯出設定
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
} 