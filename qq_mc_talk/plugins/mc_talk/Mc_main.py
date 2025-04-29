import json
import asyncio
import base64
import websockets
from nonebot import get_driver, get_bot
import nonebot

# 从配置中读取ChatBridge信息
config = get_driver().config
CHATBRIDGE_WS = getattr(config, "chatbridge_ws", "ws://36.50.226.44:8000/websocket/minecraft")
CLIENT_NAME = getattr(config, "client_name", "生存")
CLIENT_TOKEN = getattr(config, "client_token", "stardust2016")

# 全局变量，用于共享WebSocket连接
ws_connection = None

# 编码headers，模拟Java的utils.encode
def encode_headers(headers):
    headers_json = json.dumps(headers, ensure_ascii=False)
    return base64.b64encode(headers_json.encode("utf-8")).decode("utf-8")

# 准备请求头
headers = {
    "type": "Spigot",
    "info": encode_headers({"name": CLIENT_NAME, "token": CLIENT_TOKEN})
}

# 接收MC消息并通过事件机制通知其他插件
async def Mc_ws_connect():
    global ws_connection
    while True:
        try:
            async with websockets.connect(CHATBRIDGE_WS) as ws:
                ws_connection = ws
                nonebot.logger.info("Connected to ChatBridge WebSocket")
                while True:
                    try:
                        message = await ws.recv()
                        data = json.loads(message)
                        if data.get("type") == "chat":
                            player = data.get("player", "Unknown")
                            content = data.get("message", "")
                            # 通过事件机制通知 qq_talk
                            bot = get_bot()
                            await bot.call_api("send_group_msg", group_id=bot.config.target_group_id, message=f"[MC] {player}: {content}")
                    except websockets.ConnectionClosed:
                        nonebot.logger.warning("ChatBridge WebSocket disconnected, reconnecting...")
                        break
                    except Exception as e:
                        nonebot.logger.error(f"ChatBridge error: {e}")
        except Exception as e:
            nonebot.logger.error(f"Failed to connect to ChatBridge: {e}")
            await asyncio.sleep(5)  # 等待5秒后重试

# 提供接口给其他插件发送消息到MC
async def older_mc_send(player: str, message: str):
    global ws_connection
    if ws_connection is None:
        nonebot.logger.error("WebSocket connection not established")
        return
    try:
        await ws_connection.send(json.dumps({
            "type": "chat",
            "player": player,
            "message": message
        }, ensure_ascii=False))
    except Exception as e:
        nonebot.logger.error(f"Failed to send message to MC: {e}")

# 使用异步函数直接在on_startup中运行
@get_driver().on_startup
async def start_ws_connect():
    await Mc_ws_connect()

#older_mc_send