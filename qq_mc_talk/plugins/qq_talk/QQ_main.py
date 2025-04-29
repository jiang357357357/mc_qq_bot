from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.params import CommandArg
from nonebot.typing import T_State
from plugins.mc_talk import older_mc_send

# 从配置中读取目标QQ群ID
TARGET_GROUP_ID = 123456789  # 替换为你的QQ群ID，也可以通过.env配置

# 处理QQ群消息，转发到MC
matcher = on_message()
@matcher.handle()
async def handle_group_message(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.group_id != TARGET_GROUP_ID:
        return
    msg = str(event.get_message())
    if msg.startswith("!say "):  # 特定前缀触发
        content = msg[5:].strip()
        try:
            await older_mc_send("QQBot", f"[QQ] {event.sender.nickname}: {content}")
            await bot.send_group_msg(
                group_id=TARGET_GROUP_ID,
                message="消息已发送到MC哦~"
            )
        except Exception as e:
            await bot.send_group_msg(
                group_id=TARGET_GROUP_ID,
                message=f"转发到MC失败啦~错误：{e}"
            )

# # 查询服务器状态（示例，需ChatBridge支持）
# status = on_command("status", aliases={"mcstatus"})
# @status.handle()
# async def handle_status(bot: Bot, event: GroupMessageEvent, args: CommandArg):
#     if event.group_id != TARGET_GROUP_ID:
#         return
#     # 这里是示例，实际需通过ChatBridge API获取状态
#     await bot.send_group_msg(
#         group_id=TARGET_GROUP_ID,
#         message="服务器状态：在线玩家 5/20，TPS 19.8（示例）"
#     )