import os
import json

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志配置
LOG_CONFIG = {
    'log_dir': os.path.join(BASE_DIR, "logs"),
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# QQ音乐下载配置
DOWNLOAD_CONFIG = {
    'target_dir': os.path.expanduser("~/Music"),  # 目标下载目录 - 为兼容旧代码添加
    'download_dir': os.path.expanduser("~/Music"),  # 默认下载目录
    'cookie_path': os.path.join(BASE_DIR, "config", "cookie.txt"),  # Cookie文件路径 - 使用相对路径
    'max_retries': 3,  # 最大重试次数
    'concurrent_limit': 5,  # 并发下载限制
    'min_delay': 1,  # 下载最小延迟（秒）
    'max_delay': 3,  # 下载最大延迟（秒）
    'download_location': os.path.expanduser("~/Music"),  # 下载位置配置
    'format': 'bestaudio/best',  # 音频格式
    'supported_extensions': ['.mp3', '.flac', '.m4a', '.wav', '.aac']  # 支持的音频格式
}

# 加载用户配置文件
def load_user_config():
    config_path = os.path.join(os.path.dirname(__file__), 'user_settings.json')
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # 只更新下载位置配置
                if 'download_location' in user_config:
                    DOWNLOAD_CONFIG['download_location'] = user_config['download_location']
                    DOWNLOAD_CONFIG['target_dir'] = user_config['download_location']  # 同步更新target_dir
        except Exception:
            pass  # 如果加载失败，使用默认配置

# 保存用户配置
def save_config():
    config_path = os.path.join(os.path.dirname(__file__), 'user_settings.json')
    try:
        import json
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({
                'download_location': DOWNLOAD_CONFIG['download_location']
            }, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置失败: {e}")

# 检查下载位置是否有效
def is_download_location_valid():
    download_loc = DOWNLOAD_CONFIG.get('download_location', DOWNLOAD_CONFIG['download_dir'])
    return os.path.isdir(download_loc) and os.access(download_loc, os.W_OK)

# 更新下载位置
def update_download_location(new_path):
    if os.path.isdir(new_path) and os.access(new_path, os.W_OK):
        DOWNLOAD_CONFIG['download_location'] = new_path
        DOWNLOAD_CONFIG['target_dir'] = new_path  # 同步更新target_dir
        save_config()
        return True
    return False

# 加载用户配置
load_user_config()

# 初始化时检查配置文件是否存在下载位置设置
if 'download_location' not in DOWNLOAD_CONFIG:
    DOWNLOAD_CONFIG['download_location'] = DOWNLOAD_CONFIG['download_dir']

# 多线程配置
THREAD_CONFIG = {
    'max_workers': 5,  # 默认最大线程数
    'timeout': 300,    # 任务超时时间(秒)
    'task_timeout': 120,  # 单个任务超时时间(秒)
}

# 日志配置
LOG_CONFIG = {
    'log_dir': os.path.join(BASE_DIR, "logs"),
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# API配置
API_CONFIG = {
    'qq_music_base_url': 'https://y.qq.com',
    'playlist_api': 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg',
    'headers': {
        'referer': 'https://y.qq.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
}

# 风控配置
ANTI_DETECTION_CONFIG = {
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
    ],
    'request_headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
}

# 网络超时配置
NETWORK_CONFIG = {
    'socket_timeout': 30,      # Socket连接超时(秒)
    'connection_timeout': 10,  # 连接超时(秒)
    'read_timeout': 30,        # 读取超时(秒)
    'retry_count': 3,          # 重试次数
    'retry_delay_base': 2,     # 重试基础延迟(秒)
}