import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 下载配置
DOWNLOAD_CONFIG = {
    'target_dir': r'C:\Users\Prologue\Music',
    'cookie_path': os.path.join(BASE_DIR, "cookies_y.qq.com.txt"),
    'format': 'bestaudio/best',
    'supported_extensions': ['.mp3', '.flac', '.m4a', '.wav', '.aac'],
    'max_retries': 3,
    'min_delay': 1,  # 最小下载延迟(秒)
    'max_delay': 3,  # 最大下载延迟(秒)
}

# 多线程配置
THREAD_CONFIG = {
    'max_workers': 5,  # 默认最大线程数
    'timeout': 300,    # 任务超时时间(秒)
    'task_timeout': 120,  # 单个任务超时时间(秒)
}

# 日志配置
LOG_CONFIG = {
    'log_dir': os.path.join(BASE_DIR, "logs"),
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    'log_level': 'INFO',
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