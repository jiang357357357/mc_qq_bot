from nonebot.plugin import PluginMetadata

from .webhook import receive_hfish_webhook

__plugin_meta__ = PluginMetadata(
    name="webhook服务运行插件",
    description="用来接受webhook的信息",
    usage="",
    type="application",
    config=[receive_hfish_webhook],
    extra={},
)