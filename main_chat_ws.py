'''
公共頻道外接系統 — 即時抓包 + WebSocket 推播 (無 GUI 版)
-------------------------------------------------
* LIVE_CAPTURE=True 時使用 Scapy AsyncSniffer 監聽 tcp/32800
* 所有解析結果經由 WebSocket 推播給 Web 前端
'''

import re, struct, sys, time, threading, asyncio, json, datetime
from pathlib import Path
from scapy.all import AsyncSniffer, TCP
import websockets
from queue import Queue
from collections import deque
import os

# ======== 設定 ========
LIVE_CAPTURE = True
PORT = 32800
BPF_FILTER = "tcp"
WEBSOCKET_PORT = 8765

# 設定顯示分鐘數（前端會控制實際顯示，這裡主要用於歷史檔案清理）
BROADCAST_MINUTES = 120  # 預設值，前端可以獨立設定
# 將歷史檔案存在項目目錄中，方便web讀取
HISTORY_FILE = "history_messages.json"

# ======== 封包解析核心 ========
class ChatParser:
    KNOWN = {"Nickname", "Channel", "Text", "Type", "ProfileCode", "UserId"}

    @staticmethod
    def _parse_struct(data: bytes) -> dict:
        out, colors = {}, []
        i, L = 0, len(data)
        MAX_VAL_LEN = 256

        while i + 4 <= L:
            name_len = int.from_bytes(data[i:i+4], "little")
            if not 0 < name_len <= 64 or i + 4 + name_len + 6 > L:
                i += 1
                continue

            try:
                name = data[i+4:i+4+name_len].decode("ascii")
            except UnicodeDecodeError:
                i += 1
                continue

            cur = i + 4 + name_len
            type_tag = int.from_bytes(data[cur:cur+2], "little")
            val_len = int.from_bytes(data[cur+2:cur+6], "little")
            v_start, v_end = cur + 6, cur + 6 + val_len

            if v_end > L or val_len > MAX_VAL_LEN:
                i += 1
                continue

            if name != "Channel":
                if name in ChatParser.KNOWN:
                    if type_tag == 4:
                        try:
                            out[name] = data[v_start:v_end].decode("utf-8", "replace")
                        except Exception:
                            out[name] = "[INVALID UTF8]"
                elif name.startswith("#") and name_len == 7:
                    colors.append(name)

            i = v_end

        if colors:
            out["color1"] = colors[0]
        if len(colors) > 1:
            out["color2"] = colors[1]

        # 新增時間戳
        now = datetime.datetime.now()
        out["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")

        # 精確抓頻道（尾段特徵：02 XX XX XX XX 04）
        for k in range(len(data) - 6):
            if data[k] == 0x02 and data[k+5] == 0x04:
                val = int.from_bytes(data[k+1:k+5], "little")
                if 1 <= val <= 9999:
                    out["Channel"] = f"CH{val}"
                    break

        return out


    @classmethod
    def parse_packet_bytes(cls, blob: bytes) -> dict:
        return cls._parse_struct(blob[8:])  # 去掉 'TOZ ' + size

# ======== WebSocket Server ========
broadcast_queue = Queue()
clients = set()
cleanup_counter = 0  # 清理計數器
# 歷史訊息緩衝區，存最近 N 分鐘的訊息
history_messages = deque()
history_lock = threading.Lock()

def cleanup_history_file():
    """清理歷史檔案，只保留 BROADCAST_MINUTES 內的訊息"""
    if not os.path.exists(HISTORY_FILE):
        return
    
    now = datetime.datetime.now()
    valid_messages = []
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    msg = json.loads(line)
                    ts = msg.get("timestamp", "").replace("[","").replace("]","")
                    if ts:
                        try:
                            msg_time = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                            if (now - msg_time).total_seconds() <= BROADCAST_MINUTES * 60:
                                valid_messages.append(msg)
                        except Exception:
                            continue
                except Exception:
                    continue
        
        # 重新寫入有效訊息
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            for msg in valid_messages:
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")
                
        print(f"🧹 清理歷史檔案，保留 {len(valid_messages)} 條有效訊息")
    except Exception as e:
        print(f"❌ 歷史檔案清理失敗: {e}")

async def websocket_handler(websocket):
    clients.add(websocket)
    # 新連線時主動推送歷史訊息（從檔案讀取）
    now = datetime.datetime.now()
    count = 0
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        msg = json.loads(line)
                        # 過濾 BROADCAST_MINUTES 內的訊息
                        ts = msg.get("timestamp", "").replace("[","").replace("]","")
                        if ts:
                            try:
                                msg_time = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                                if (now - msg_time).total_seconds() > BROADCAST_MINUTES * 60:
                                    continue
                            except Exception:
                                continue
                        await websocket.send(json.dumps(msg, ensure_ascii=False))
                        count += 1
                    except Exception:
                        continue
        except Exception as e:
            print(f"❌ 歷史訊息讀取失敗: {e}")
    print(f"📡 新客戶端連線，推送 {count} 條歷史訊息 (file cache)")
    try:
        while True:
            msg = await asyncio.get_event_loop().run_in_executor(None, broadcast_queue.get)
            for client in clients.copy():
                try:
                    await client.send(msg)
                except:
                    clients.remove(client)
    finally:
        clients.discard(websocket)

async def websocket_server():
    async with websockets.serve(websocket_handler, "0.0.0.0", WEBSOCKET_PORT):
        print(f"✅ WebSocket 推播伺服器啟動於 ws://localhost:{WEBSOCKET_PORT}")
        await asyncio.Future()  # run forever

# ======== Scapy Sniffer ========
def handle_packet(pkt):
    global cleanup_counter
    if TCP not in pkt: return
    payload = bytes(pkt[TCP].payload)
    if not payload:
        return
    # 顯示 16 進制內容
    # print("[封包 16進制內容]")
    # for i in range(0, len(payload), 16):
    #     chunk = payload[i:i+16]
    #     hex_part = ' '.join(f"{b:02X}" for b in chunk)
    #     ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
    #     print(f"{i:04X}  {hex_part:<47}  {ascii_part}")
    # print("[封包結束]\n")

    # 自動偵測格式並推播
    idx = payload.find(b"TOZ ")
    while idx >= 0 and idx + 8 <= len(payload):
        size = int.from_bytes(payload[idx+4:idx+8], "little")
        if idx + 8 + size > len(payload): break
        blob = payload[idx:idx+8+size]
        try:
            parsed_list = ChatParser.parse_packet_bytes(blob)
            for parsed in parsed_list:
                if parsed.get("Nickname") or parsed.get("Text"):
                    # 存進檔案緩衝區
                    try:
                        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                            f.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                        print(f"寫入歷史訊息到 {HISTORY_FILE}")
                        
                        # 每 10 次寫入清理一次歷史檔案
                        cleanup_counter += 1
                        if cleanup_counter >= 10:
                            cleanup_counter = 0
                            cleanup_history_file()
                    except Exception as e:
                        print(f"❌ 歷史訊息寫入失敗: {e}")
                    broadcast_queue.put(json.dumps(parsed, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 解析失敗：{e}")
        idx = payload.find(b"TOZ ", idx + 1)
    else:
        try:
            parsed = ChatParser.parse_packet_bytes(payload)
            if parsed.get("Nickname") or parsed.get("Text"):
                # 存進檔案緩衝區
                try:
                    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                        f.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                    print(f"寫入歷史訊息到 {HISTORY_FILE}")
                    
                    # 每 10 次寫入清理一次歷史檔案
                    cleanup_counter += 1
                    if cleanup_counter >= 10:
                        cleanup_counter = 0
                        cleanup_history_file()
                except Exception as e:
                    print(f"❌ 歷史訊息寫入失敗: {e}")
                broadcast_queue.put(json.dumps(parsed, ensure_ascii=False))
        except Exception as e:
            print(f"❌ 解析失敗：{e}")

# ======== 主程式 ========
if __name__ == "__main__":
    print(f">> 🟢 啟動 Sniffer 中（{BPF_FILTER}） ✅ 已啟動 MapleStory 聊天 WebSocket 推播器")
    threading.Thread(target=lambda: AsyncSniffer(filter=BPF_FILTER, prn=handle_packet, store=False).start(), daemon=True).start()
    asyncio.run(websocket_server())
