from nonebot.plugin import PluginMetadata

from .main import main_run
# from plugins.mc_talk.Mc_main import Mc_ws_connect, older_mc_send
# from plugins.qq_talk.QQ_main import handle_group_message
from plugins.webhook.webhook import receive_hfish_webhook

__plugin_meta__ = PluginMetadata(
    name="主要运行插件",
    description="用来运行所有服务",
    usage="",
    type="application",
    config=[main_run],
    extra={},
)