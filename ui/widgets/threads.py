# -*- coding: utf-8 -*-
"""
线程模块，包含后台处理线程
"""

from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import yt_dlp
from utils.logger import success_count, failure_count, reset_stats


class ProgressCallback:
    """用于下载进度回调的类"""
    def __init__(self, worker, song_id, song_title):
        self.worker = worker
        self.song_id = song_id
        self.song_title = song_title

    def __call__(self, d):
        if d['status'] == 'downloading':
            # 获取下载信息
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            if total_bytes > 0:
                percentage = (downloaded_bytes / total_bytes) * 100
                downloaded_mb = downloaded_bytes / (1024 * 1024)
                total_mb = total_bytes / (1024 * 1024)
                # 使用实际歌名作为标识
                self.worker.progress_updated.emit(f"{self.song_id}::{self.song_title}", int(percentage), downloaded_mb, total_mb)
        elif d['status'] == 'finished':
            # 下载完成，发送完成信号，使用实际歌名
            self.worker.download_finished.emit(f"{self.song_id}::{self.song_title}", True)


class DownloadWorker(QObject):
    """下载工作线程"""
    progress_updated = pyqtSignal(str, int, float, float)  # 歌曲ID, 百分比, 已下载MB, 总MB
    download_finished = pyqtSignal(str, bool)  # 歌曲ID, 是否成功
    all_finished = pyqtSignal(int, int)  # 成功数, 失败数
    error_occurred = pyqtSignal(str)  # 错误信息

    def __init__(self, service_type, input_value):
        super().__init__()
        self.service_type = service_type
        self.input_value = input_value

    def _download_with_callback(self, downloader, song_id, callback):
        """使用回调函数下载单个文件"""
        # 构建URL
        url = downloader._build_qq_music_url(song_id)
        
        # 检查输入有效性
        if not song_id or len(str(song_id)) > 100:
            print("❌ 输入无效：歌曲ID为空或过长")
            return False, "invalid_input"
            
        # 检查是否为歌曲名而非ID
        if not downloader._is_valid_song_id(song_id):
            print(f"❌ 输入可能是歌曲名而非ID: {song_id}")
            print("💡 请提供正确的歌曲ID（如：004R7qfh1ALctJ）")
            return False, "invalid_input"
        
        retries = downloader.max_retries
        
        for attempt in range(retries):
            try:
                # 重试间隔延迟
                if attempt > 0:
                    delay = min(2 ** attempt, 30)
                    print(f"⏳ 等待 {delay} 秒后重试...")
                
                ydl_opts = downloader.get_ydl_options()
                ydl_opts['user_agent'] = downloader.get_random_user_agent()
                
                # 从配置中获取下载位置
                from config.settings import DOWNLOAD_CONFIG
                download_location = DOWNLOAD_CONFIG.get('download_location', DOWNLOAD_CONFIG['download_dir'])
                ydl_opts['outtmpl'] = os.path.join(download_location, '%(title)s.%(ext)s')
                
                print(f"[{attempt+1}/{retries}] 🎵 正在连接...")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 先获取信息
                    try:
                        info = ydl.extract_info(url, download=False)
                        current_title = info['title']
                    except Exception as e:
                        if "timed out" in str(e).lower():
                            print(f"⏰ 连接超时，正在重试...")
                            if attempt < retries - 1:
                                continue
                        elif "Unsupported URL" in str(e) or "not found" in str(e).lower():
                            print(f"❌ 没有找到: {song_id}")
                            return False, "not_found"
                        else:
                            print(f"❌ 获取歌曲信息失败: {str(e)}")
                            return False, "other_error"
                    
                    # 检查文件是否存在
                    if downloader.check_file_exists(current_title):
                        print(f"📁 已存在: {current_title}")
                        return "exists", current_title
                    
                    print(f"[{attempt+1}/{retries}] 🎵 开始下载: {current_title}")
                    
                    # 创建带正确参数的ProgressCallback
                    callback = ProgressCallback(self, song_id, current_title)
                    
                    # 执行下载
                    ydl_params = downloader.get_ydl_options(callback)
                    ydl_params['user_agent'] = downloader.get_random_user_agent()
                    
                    # 同样设置下载位置
                    ydl_params['outtmpl'] = os.path.join(download_location, '%(title)s.%(ext)s')
                    
                    try:
                        with yt_dlp.YoutubeDL(ydl_params) as ydl_with_progress:
                            ydl_with_progress.download([url])
                    except Exception as e:
                        if "timed out" in str(e).lower():
                            print(f"⏰ 下载超时，正在重试...")
                            if attempt < retries - 1:
                                continue
                        elif "not available for registered users" in str(e).lower():
                            print(f"❌ 需要登录: {current_title}")
                            return False, "login_required"
                        else:
                            print(f"❌ 下载失败: {str(e)}")
                            return False, "download_error"
                    
                    # 添加下载延迟
                    from utils.logger import add_download_delay
                    from config.settings import DOWNLOAD_CONFIG
                    add_download_delay(
                        DOWNLOAD_CONFIG['min_delay'], 
                        DOWNLOAD_CONFIG['max_delay']
                    )
                    
                    print(f"✅ 完成: {current_title}")
                    return True, current_title
                    
            except Exception as e:
                error_msg = str(e)
                if "timed out" in error_msg.lower():
                    print(f"[{attempt+1}/{retries}] ⏰ 超时: 网络连接超时")
                else:
                    print(f"[{attempt+1}/{retries}] ❌ 失败: {error_msg}")
                
                if attempt == retries - 1:
                    from utils.logger import log_failure, update_stats
                    log_failure("music_download", error_msg, url)
                    update_stats(False)
        
        print(f"🔄 已达到最大重试次数({retries})，跳过该歌曲")
        return False, "retry_limit_exceeded"

    def run_download(self):
        try:
            from core.downloader import MusicDownloader
            from core.multithread_downloader import MultithreadDownloader
            from core.qq_music_api import QQMusicAPI
            from utils.logger import success_count, failure_count, reset_stats
            import os

            # 重置统计
            reset_stats()

            # 准备下载列表
            if self.service_type == "playlist":
                # 解析歌单
                api = QQMusicAPI()
                song_ids = api.get_playlist_song_ids(self.input_value)
                if not song_ids:
                    self.error_occurred.emit("无法获取歌单中的歌曲，请检查链接是否正确")
                    return
            else:
                # 单曲下载，按照空格分割
                song_ids = [id.strip() for id in self.input_value.split() if id.strip()]
                if not song_ids:
                    self.error_occurred.emit("请输入至少一个歌曲ID")
                    return

            # 逐一下载歌曲
            downloader = MusicDownloader()
            
            # 记录结果
            successful = 0
            failed = 0
            
            # 逐一下载歌曲
            for song_id in song_ids:
                try:
                    # 先获取歌曲信息以获得实际歌名
                    url = downloader._build_qq_music_url(song_id)
                    ydl_opts = downloader.get_ydl_options()
                    ydl_opts['user_agent'] = downloader.get_random_user_agent()
                    
                    # 设置下载位置
                    from config.settings import DOWNLOAD_CONFIG
                    download_location = DOWNLOAD_CONFIG.get('download_location', DOWNLOAD_CONFIG['download_dir'])
                    ydl_opts['outtmpl'] = os.path.join(download_location, '%(title)s.%(ext)s')
                    
                    import yt_dlp
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            info = ydl.extract_info(url, download=False)
                            current_title = info['title']
                        except:
                            # 如果获取失败，使用ID作为标题
                            current_title = song_id
                    
                    # 创建进度回调，使用获取到的实际歌名
                    callback = ProgressCallback(self, song_id, current_title)
                    # 下载并获取结果和状态
                    result, status_or_title = self._download_with_callback(downloader, song_id, callback)
                    
                    if result == "exists":
                        # 文件已存在
                        self.download_finished.emit(f"{song_id}::{status_or_title} (已存在)", True)
                        successful += 1
                    elif result:
                        # 下载成功
                        self.download_finished.emit(f"{song_id}::{status_or_title}", True)
                        successful += 1
                    else:
                        # 下载失败，根据状态返回不同消息
                        if status_or_title == "not_found":
                            self.download_finished.emit(f"{song_id}::没有找到", False)
                        elif status_or_title in ["invalid_input", "login_required", "download_error", "retry_limit_exceeded", "other_error"]:
                            self.download_finished.emit(f"{song_id}::下载失败，请参考帮助", False)
                        else:
                            self.download_finished.emit(f"{song_id}::下载失败，请参考帮助", False)
                        failed += 1
                        
                except Exception as e:
                    # 下载失败
                    self.download_finished.emit(f"{song_id}::下载失败，请参考帮助", False)
                    failed += 1
                    
            # 下载完成后获取最新统计
            from utils.logger import success_count, failure_count
            self.all_finished.emit(success_count, failure_count)
        except Exception as e:
            self.error_occurred.emit(str(e))