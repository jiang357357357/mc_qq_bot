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
    # 获取请求头和 body
    headers = request.headers
    body = await request.json()

    # 简单 token 验证（可选，建议在 HFish 后台配置相同的 token）
    # expected_token = "你的WebhookToken"  # 替换为你的 token
    # received_token = headers.get("X-HFish-Token", "")
    # if expected_token and received_token != expected_token:
    #     logger.warning("Webhook 验证失败，token 不匹配！")
    #     raise HTTPException(status_code=403, detail="token 错误")

    # 解析 Webhook 数据
    try:
        payload = HFishWebhookPayload(**body)
        logger.info(f"收到 HFish Webhook: 事件 ID={payload.event_id}, 攻击 IP={payload.attack_ip}")

        # 格式化攻击信息
        message = (
            f"🚨 蜜罐捕获到攻击！\n"
            f"📅 时间: {payload.attack_time}\n"
            f"🌐 攻击 IP: {payload.attack_ip}:{payload.attack_port}\n"
            f"🎯 蜜罐: {payload.honeypot_ip}:{payload.honeypot_port}\n"
            f"🔗 协议: {payload.protocol}\n"
            f"⚔️ 类型: {payload.attack_type}\n"
            f"📝 详情: {payload.details}"
        )

        # 获取 NoneBot 机器人实例
        bot = get_bot()

        # 发送到群聊（替换为你的群号）
        await bot.send_group_msg(
            group_id=123456789,  # 替换为你的群号
            message=message
        )

        # （可选）可以在这里添加其他逻辑，比如存数据库
        # await save_to_database(payload)

        return {"status": "success", "message": "HFish Webhook 接收成功"}
    except Exception as e:
        logger.error(f"处理 HFish Webhook 失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理出错: {str(e)} ")
