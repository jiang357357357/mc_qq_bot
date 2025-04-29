import nonebot
from nonebot.adapters.onebot.v11 import Adapter
import os
import sys
from nonebot.plugin import Plugin

from pathlib import Path


# 获取 bot.py 所在的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 使用相对路径加载 .env 和 pyproject.toml
ENV_PATH = os.path.join(BASE_DIR, ".env")
TOML_PATH = os.path.join(BASE_DIR, "pyproject.toml")

# 检查文件是否存在
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"找不到本项目的环境变量 {ENV_PATH}")
if not os.path.exists(TOML_PATH):
    raise FileNotFoundError(f"无法找到 {TOML_PATH}")

# 将项目目录添加到 sys.path 中，以便导入其他模块
nonebot.init(_env_file=ENV_PATH)
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_from_toml(TOML_PATH)

if __name__ == "__main__":
    # 等待上面项目加载完成，后载入插件
    plugin: Plugin | None = nonebot.get_plugin("main")
    from plugins.main.main import main_run
    # main_run()
    # 运行
    nonebot.run()