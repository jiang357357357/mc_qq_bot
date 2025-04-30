import nonebot
from nonebot.adapters.onebot.v11 import Bot
from nonebot import get_driver, get_bot
from nonebot.log import logger
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional


# 输出信息
logger.info("webhook插件加载完成")

# 定义要发送的指定群聊


# 获取 FastAPI 实例
app: FastAPI = get_driver().server_app

# 定义 HFish Webhook 的数据模型
class HFishWebhookPayload(BaseModel):
    event_id: str
    attack_time: str
    attack_ip: str
    attack_port: int
    honeypot_ip: str
    honeypot_port: int
    protocol: str
    attack_type: str
    details: dict

# Webhook 路由，专门处理 HFish 事件
@app.post("/hfish_webhook")
async def receive_hfish_webhook(request: Request):
   # 先获取原始数据
    raw_body = await request.body()
    print("收到HFish原始数据:", raw_body)

    # 尝试解析JSON
    try:
        data = await request.json()
        print("解析后的HFish数据:", data)
    except Exception as e:
        print("JSON解析失败:", str(e))
        return {"status": "error", "message": "Invalid JSON"}

    bot: Bot = nonebot.get_bot()
    await bot.send_group_msg(
        group_id=123456789,  # 改成你的QQ群号
        message=f"⚠️ 检测到攻击！\n"
                f"时间: {data.get('create_time', '未知')}\n"
                f"类型: {data.get('type', '未知')}\n"
                f"IP: {data.get('src_ip', '未知')}"
    )
    return {"status": "success"}
