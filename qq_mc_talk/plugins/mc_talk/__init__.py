from nonebot.plugin import PluginMetadata

from .Mc_main import Mc_ws_connect, older_mc_send

__plugin_meta__ = PluginMetadata(
    name="MC服务运行插件",
    description="用来运行Mc服务",
    usage="",
    type="application",
    config=[Mc_ws_connect, older_mc_send],
    extra={},
)