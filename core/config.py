import json
import os
import logging

logger = logging.getLogger(__name__)

# 构造配置文件的绝对路径
# __file__ 是当前文件的路径 (core/config.py)
# os.path.dirname(__file__) 是当前文件所在的目录 (core/)
# '..' 是父目录
# 'data/role_config.json' 是目标文件
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'role_config.json'))

def load_role_config():
    """从 data/role_config.json 加载角色配置"""
    if not os.path.exists(CONFIG_PATH):
        logger.warning(f"配置文件不存在于: {CONFIG_PATH}")
        return []
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"加载配置文件 {CONFIG_PATH} 失败: {e}")
        return []

def save_role_config(data):
    """将角色配置保存到 data/role_config.json（原子写入）"""
    temp_path = CONFIG_PATH + '.tmp'
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # 原子替换
        os.replace(temp_path, CONFIG_PATH)
        return True
    except IOError as e:
        logger.error(f"保存配置文件 {CONFIG_PATH} 失败: {e}")
        return False