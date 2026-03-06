import os
import yt_dlp
import time
import random
from config.settings import DOWNLOAD_CONFIG, ANTI_DETECTION_CONFIG
from utils.logger import log_failure, update_stats, add_download_delay

class ProgressHook:
    """下载进度钩子类"""
    def __init__(self, song_title=""):
        self.song_title = song_title
        self.last_update = 0
        self.update_interval = 1.0  # 更新间隔1秒
    
    def __call__(self, d):
        if d['status'] == 'downloading':
            # 获取下载信息
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            speed = d.get('speed', 0)
            
            # 转换为更友好的单位
            downloaded_mb = downloaded_bytes / (1024 * 1024)
            total_mb = total_bytes / (1024 * 1024) if total_bytes > 0 else 0
            speed_kbps = speed / 1024 if speed > 0 else 0
            
            # 控制更新频率
            current_time = time.time()
            if current_time - self.last_update >= self.update_interval:
                if total_bytes > 0:
                    percentage = (downloaded_bytes / total_bytes) * 100
                    print(f"\r🎵 {self.song_title} 下载中: {percentage:.1f}% ({downloaded_mb:.1f}/{total_mb:.1f}MB) {speed_kbps:.1f}KB/s", end='', flush=True)
                else:
                    print(f"\r🎵 {self.song_title} 下载中: {downloaded_mb:.1f}MB downloaded ({speed_kbps:.1f}KB/s)", end='', flush=True)
                self.last_update = current_time
                
        elif d['status'] == 'finished':
            print(f"\r✅ {self.song_title} 下载完成!{' ' * 50}")  # 清除进度行

class BaseDownloader:
    """基础下载器类 - 为不同类型文件下载提供统一接口"""
    
    def __init__(self, target_dir=None, cookie_path=None):
        self.target_dir = target_dir or DOWNLOAD_CONFIG['target_dir']
        self.cookie_path = cookie_path or DOWNLOAD_CONFIG['cookie_path']
        
        # 确保目标目录存在
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
    
    def check_file_exists(self, title):
        """检查文件是否已存在"""
        extensions = DOWNLOAD_CONFIG['supported_extensions']
        for ext in extensions:
            if os.path.exists(os.path.join(self.target_dir, f"{title}{ext}")):
                return True
        return False
    
    def get_random_user_agent(self):
        """获取随机User-Agent"""
        return random.choice(ANTI_DETECTION_CONFIG['user_agents'])
    
    def get_ydl_options(self, progress_hook=None):
        """获取yt-dlp配置选项 - 减少详细输出并添加超时控制"""
        options = {
            'format': DOWNLOAD_CONFIG['format'],
            'outtmpl': os.path.join(self.target_dir, '%(title)s.%(ext)s'),
            'quiet': True,           # 减少输出
            'no_warnings': True,     # 隐藏警告
            'noprogress': True,      # 隐藏进度条
            'no_color': True,        # 禁用颜色输出
            'cookiefile': self.cookie_path,
            # 网络超时控制
            'socket_timeout': 30,    # Socket超时30秒
            'retries': 3,           # 网络重试次数
            'fragment_retries': 3,  # 分段重试次数
            'retry_sleep_functions': {
                'http': lambda n: 2 ** n,  # HTTP重试延迟
                'fragment': lambda n: 2 ** n,  # 分段重试延迟
                'file_access': lambda n: 2 ** n,  # 文件访问重试延迟
            }
        }
        
        # 添加进度钩子（如果提供）
        if progress_hook:
            options['progress_hooks'] = [progress_hook]
            
        return options
    
    def download_single_file(self, url, title=None, max_retries=None):
        """
        下载单个文件的基础方法
        子类应该重写此方法实现具体下载逻辑
        """
        raise NotImplementedError("子类必须实现download_single_file方法")


class MusicDownloader(BaseDownloader):
    """音乐下载器 - 继承基础下载器"""
    
    def __init__(self, target_dir=None, cookie_path=None):
        super().__init__(target_dir, cookie_path)
        self.max_retries = DOWNLOAD_CONFIG['max_retries']
        # 验证配置
        self._validate_config()
    
    def _validate_config(self):
        """验证配置文件的完整性"""
        errors = []
        
        # 检查下载目录
        if not self.target_dir or not os.path.exists(self.target_dir):
            errors.append("❌ 下载目录未指定或不存在")
        
        # 检查Cookie文件
        if not self.cookie_path or not os.path.exists(self.cookie_path):
            errors.append("❌ Cookie文件未指定或不存在")
        
        if errors:
            print("配置检查发现问题:")
            for error in errors:
                print(f"  {error}")
            print("请检查 config/settings.py 中的配置")
            raise ValueError("配置不完整")
    
    def _build_qq_music_url(self, song_id_or_url):
        """构建QQ音乐URL"""
        if not song_id_or_url.startswith("http"):
            return f"https://y.qq.com/n/ryqq/songDetail/{song_id_or_url}"
        return song_id_or_url
    
    def download_single_file(self, song_id_or_url, title=None, max_retries=None):
        """下载单首QQ音乐"""
        # 输入验证
        if not song_id_or_url or len(str(song_id_or_url)) > 100:
            print("❌ 输入无效：歌曲ID为空或过长")
            update_stats(False)
            return False
            
        # 检查是否为歌曲名而非ID
        if not self._is_valid_song_id(song_id_or_url):
            print(f"❌ 输入可能是歌曲名而非ID: {song_id_or_url}")
            print("💡 请提供正确的歌曲ID（如：004R7qfh1ALctJ）")
            update_stats(False)
            return False
        
        url = self._build_qq_music_url(song_id_or_url)
        retries = max_retries or self.max_retries
        
        for attempt in range(retries):
            try:
                # 重试间隔延迟（第一次不需要延迟）
                if attempt > 0:
                    # 指数退避延迟，但不超过30秒
                    delay = min(2 ** attempt, 30)
                    print(f"⏳ 等待 {delay} 秒后重试...")
                    time.sleep(delay)
                
                ydl_opts = self.get_ydl_options()
                # 添加随机User-Agent增强反检测
                ydl_opts['user_agent'] = self.get_random_user_agent()
                
                print(f"[{attempt+1}/{retries}] 🎵 正在连接...")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 先获取信息（不下载）- 添加超时控制
                    try:
                        info = ydl.extract_info(url, download=False)
                        current_title = info['title']
                    except Exception as e:
                        if "timed out" in str(e).lower():
                            print(f"⏰ 连接超时，正在重试...")
                            if attempt < retries - 1:
                                continue
                        raise e
                    
                    # 检查文件是否存在
                    if self.check_file_exists(current_title):
                        print(f"📁 已存在: {current_title}")
                        # 文件已存在不算作新的成功统计
                        return True
                    
                    print(f"[{attempt+1}/{retries}] 🎵 开始下载: {current_title}")
                    
                    # 创建进度钩子并执行下载
                    progress_hook = ProgressHook(current_title)
                    ydl_params = self.get_ydl_options(progress_hook)
                    ydl_params['user_agent'] = self.get_random_user_agent()
                    
                    # 执行下载 - 添加超时控制
                    try:
                        with yt_dlp.YoutubeDL(ydl_params) as ydl_with_progress:
                            ydl_with_progress.download([url])
                    except Exception as e:
                        if "timed out" in str(e).lower():
                            print(f"⏰ 下载超时，正在重试...")
                            if attempt < retries - 1:
                                continue
                        raise e
                    
                    # 添加下载延迟减少被封风险
                    add_download_delay(
                        DOWNLOAD_CONFIG['min_delay'], 
                        DOWNLOAD_CONFIG['max_delay']
                    )
                    
                    print(f"✅ 完成: {current_title}")
                    update_stats(True)  # 更新成功统计
                    return True
                    
            except Exception as e:
                error_msg = str(e)
                if "timed out" in error_msg.lower():
                    print(f"[{attempt+1}/{retries}] ⏰ 超时: 网络连接超时")
                else:
                    print(f"[{attempt+1}/{retries}] ❌ 失败: {error_msg}")
                
                # 只在最后一次尝试失败时记录日志
                if attempt == retries - 1:
                    log_failure("music_download", error_msg, url)
                    update_stats(False)  # 更新失败统计
        
        print(f"🔄 已达到最大重试次数({retries})，跳过该歌曲")
        return False
    
    def _is_valid_song_id(self, input_str):
        """检查输入是否为有效的歌曲ID格式"""
        # QQ音乐ID通常是字母数字组合，长度在10-20之间
        if not isinstance(input_str, str):
            return False
        
        # 基本格式检查
        if len(input_str) < 10 or len(input_str) > 20:
            return False
            
        # 检查是否包含明显的歌曲名特征
        song_name_indicators = [' ', '-', '_', '(', ')', '【', '】', '《', '》']
        for indicator in song_name_indicators:
            if indicator in input_str:
                return False
                
        # 检查是否为纯数字（不太可能是歌曲ID）
        if input_str.isdigit() and len(input_str) < 15:
            return False
            
        return True


# TODO: 其他类型文件下载器可以在这里扩展
# class VideoDownloader(BaseDownloader):
#     """视频下载器"""
#     pass

# class DocumentDownloader(BaseDownloader):
#     """文档下载器"""
#     pass