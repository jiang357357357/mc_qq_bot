from nonebot.plugin import PluginMetadata

from .QQ_main import handle_group_message

__plugin_meta__ = PluginMetadata(
    name="qq服务运行插件",
    description="用来运行qq服务",
    usage="",
    type="application",
    config=[handle_group_message],
    extra={},
)