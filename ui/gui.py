import sys
import os
# 添加项目根目录到Python路径，以便正确导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QScrollArea, QLineEdit, QProgressBar, QFrame,
    QMenuBar, QMenu, QSizePolicy, QToolButton, QDialog, QListWidget, QListWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QSequentialAnimationGroup, QPoint, QParallelAnimationGroup, QThread, QObject, pyqtSlot
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QColor


class AgreementDialog(QDialog):
    """使用须知弹窗"""
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("使用须知")
        self.setMinimumSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("使用须知")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 富文本内容区域
        content_area = QScrollArea()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setHtml("""
        <div style="font-size: 12px; font-weight: bold;">
        <p>本产品仅供学习使用，切勿用于非法用途。</p>
        <br>
        <p><strong>功能：</strong>支持下载歌单内所有歌曲 / 单曲（请结合 README 摘要）。</p>
        <br>
        <p><strong>其他注意事项：</strong></p>
        <ul>
          <li>本工具仅支持QQ音乐平台的音乐下载</li>
          <li>使用过程中请确保您的Cookie文件有效</li>
          <li>下载大量音乐时请注意网络状况和存储空间</li>
          <li>请遵守相关法律法规，合理使用本工具</li>
          <li>不当使用可能违反服务条款，建议仅用于个人学习与备份</li>
        </ul>
        <br>
        <p>使用本工具即表示您同意以上条款。</p>
        </div>
        """)
        content_layout.addWidget(content_text)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        main_layout.addWidget(content_area)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        agree_btn = QPushButton("我已知晓并同意")
        agree_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #4CAF50;"
            "   color: white;"
            "   border: none;"
            "   padding: 8px 20px;"
            "   border-radius: 4px;"
            "   font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "   background-color: #45a049;"
            "}"
        )
        agree_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("退出")
        cancel_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #f44336;"
            "   color: white;"
            "   border: none;"
            "   padding: 8px 20px;"
            "   border-radius: 4px;"
            "   font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "   background-color: #da190b;"
            "}"
        )
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(agree_btn)
        button_layout.addWidget(cancel_btn)

        main_layout.addLayout(button_layout)


class ServiceSelectionWidget(QWidget):
    """服务选择界面"""
    service_selected = pyqtSignal(str)  # 发送选择的服务类型
    go_back = pyqtSignal()  # 返回信号

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 提示文字容器
        self.prompt_container = QWidget()
        prompt_layout = QHBoxLayout(self.prompt_container)
        prompt_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.char_labels = []
        
        text = "请选择您需要的服务"
        for i, char in enumerate(text):
            label = QLabel(char)
            label.setProperty("char_index", i)
            # 初始为完全透明（不可见）
            label.setStyleSheet("color: rgba(255, 165, 0, 0); font-weight: bold; font-size: 16px;")
            label.setFont(QFont("SimSun", 16, QFont.Weight.Bold))
            label.setMinimumWidth(25)
            # 确保标签被添加到布局中
            prompt_layout.addWidget(label)
            self.char_labels.append(label)
        
        # 初始隐藏容器，在动画开始时再显示
        self.prompt_container.hide()
        main_layout.addWidget(self.prompt_container)

        # 服务按钮容器
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 歌单下载按钮
        self.playlist_btn = QPushButton("下载歌单内所有歌曲")
        self.playlist_btn.setObjectName("playlistBtn")
        self.playlist_btn.setStyleSheet(
            "QPushButton {"
            "   border: none;"
            "   font-size: 14px;"
            "   color: #333;"
            "   padding: 10px 20px;"
            "}"
            "QPushButton:hover {"
            "   text-decoration: underline;"
            "   color: #007ACC;"
            "}"
        )
        self.playlist_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.playlist_btn.clicked.connect(lambda: self.service_selected.emit("playlist"))
        button_layout.addWidget(self.playlist_btn)

        # 单曲下载按钮
        self.song_btn = QPushButton("下载我需要的歌曲")
        self.song_btn.setObjectName("songBtn")
        self.song_btn.setStyleSheet(
            "QPushButton {"
            "   border: none;"
            "   font-size: 14px;"
            "   color: #333;"
            "   padding: 10px 20px;"
            "}"
            "QPushButton:hover {"
            "   text-decoration: underline;"
            "   color: #007ACC;"
            "}"
        )
        self.song_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.song_btn.clicked.connect(lambda: self.service_selected.emit("song"))
        button_layout.addWidget(self.song_btn)

        button_container.hide()  # 初始隐藏，动画后显示
        main_layout.addWidget(button_container)
        self.button_container = button_container

        # 返回按钮
        back_btn = QPushButton("返回")
        back_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #f0f0f0;"
            "   border: 1px solid #ccc;"
            "   padding: 6px 15px;"
            "   border-radius: 4px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #e0e0e0;"
            "}"
        )
        back_btn.clicked.connect(self.go_back.emit)
        back_btn.setMaximumWidth(80)
        back_btn.move(10, 10)
        self.back_btn = back_btn

        # 添加占位符使返回按钮定位到右下角
        main_layout.addStretch()

        # 创建浮动布局放置返回按钮
        floating_layout = QHBoxLayout()
        floating_layout.addStretch()
        floating_layout.addWidget(back_btn)
        main_layout.addLayout(floating_layout)

    def setup_animations(self):
        # 动画组
        self.animation_group = QSequentialAnimationGroup()

        # 提示文字淡入动画
        self.prompt_fade_in = QPropertyAnimation(self.prompt_container, b"windowOpacity")
        self.prompt_fade_in.setDuration(500)
        self.prompt_fade_in.setStartValue(0)
        self.prompt_fade_in.setEndValue(1)

        # 按钮容器淡入动画
        self.buttons_fade_in = QPropertyAnimation(self.button_container, b"windowOpacity")
        self.buttons_fade_in.setDuration(500)
        self.buttons_fade_in.setStartValue(0)
        self.buttons_fade_in.setEndValue(1)

        # 添加到动画组
        self.animation_group.addPause(300)  # 短暂停顿
        self.animation_group.addAnimation(self.prompt_fade_in)
        self.animation_group.addAnimation(self.buttons_fade_in)

    def start_animation(self):
        # 先显示容器
        self.prompt_container.show()
        self.button_container.show()
        # 再启动动画组（淡入效果）
        self.animation_group.start()
        # 最后启动字符逐个显示动画
        self.start_char_animation()
    
    def start_char_animation(self):
        """启动字符逐个显示动画"""
        self.current_char_index = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.show_next_char)
        self.animation_timer.start(200)  # 每200毫秒显示下一个字符
    
    def show_next_char(self):
        """显示下一个字符，橙色状态下显示，保持橙色"""
        if self.current_char_index < len(self.char_labels):
            # 设置当前字符为橙色（显示中）
            self.char_labels[self.current_char_index].setStyleSheet(
                "color: orange; font-weight: bold; font-size: 16px;"
            )
            
            self.current_char_index += 1
        else:
            # 所有字符都显示完成后，停止定时器即可，不再改变颜色
            self.animation_timer.stop()


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
        import yt_dlp  # 添加yt_dlp导入
        
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
            from core.downloaders.downloader import MusicDownloader
            from core.downloaders.multithread_downloader import MultithreadDownloader
            from core.api.qq_music_api import QQMusicAPI
            from utils.logger import success_count, failure_count, reset_stats

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


class DownloadTaskWidget(QWidget):
    """下载任务界面"""
    go_back = pyqtSignal()  # 返回信号

    def __init__(self, service_type):
        super().__init__()
        self.service_type = service_type
        self.active_downloads = {}  # 存储活动下载的信息
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 顶部提示文字（初始是按钮文字）
        service_text = "下载歌单内所有歌曲" if self.service_type == "playlist" else "下载我需要的歌曲"
        self.top_label = QLabel(service_text)
        top_font = QFont()
        top_font.setPointSize(16)
        top_font.setBold(True)
        self.top_label.setFont(top_font)
        self.top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_label.setStyleSheet("color: #333; font-weight: bold;")
        main_layout.addWidget(self.top_label)

        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        placeholder_text = "请输入歌单链接" if self.service_type == "playlist" else "请输入歌曲 ID（多个ID用空格分隔）"
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder_text)
        self.input_field.setMinimumWidth(250)
        input_layout.addWidget(self.input_field)

        start_btn = QPushButton("开始下载")
        start_btn.clicked.connect(self.start_download)
        input_layout.addWidget(start_btn)

        main_layout.addLayout(input_layout)

        # 进度显示区域
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.progress_area = QVBoxLayout(self.scroll_widget)
        self.progress_area.setSpacing(10)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        # 返回按钮
        back_btn = QPushButton("返回")
        back_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #f0f0f0;"
            "   border: 1px solid #ccc;"
            "   padding: 6px 15px;"
            "   border-radius: 4px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #e0e0e0;"
            "}"
        )
        back_btn.clicked.connect(self.go_back.emit)
        back_btn.setMaximumWidth(80)
        main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def start_download(self):
        input_value = self.input_field.text().strip()
        if not input_value:
            QMessageBox.warning(self, "输入错误", "请输入有效的歌曲ID或歌单链接")
            return

        # 启动下载线程
        self.worker = DownloadWorker(self.service_type, input_value)
        self.thread = QThread()
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_download)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.download_finished.connect(self.on_download_finished)
        self.worker.all_finished.connect(self.on_all_finished)
        self.worker.error_occurred.connect(self.on_error)
        
        # 禁用输入字段，防止重复点击
        self.input_field.setEnabled(False)
        
        # 开始下载
        self.thread.start()

    def update_progress(self, song_id, percentage, downloaded_mb, total_mb):
        """更新特定歌曲的进度"""
        # 检查是否已经有进度组件，如果没有则创建一个
        if song_id not in self.active_downloads:
            # 创建新的进度条组件
            progress_widget = QWidget()
            progress_layout = QVBoxLayout(progress_widget)
            
            song_label = QLabel(f"正在下载: {song_id}")
            song_label.setObjectName(f"label_{song_id}")
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(percentage)
            progress_bar.setObjectName(f"progress_{song_id}")
            
            progress_layout.addWidget(song_label)
            progress_layout.addWidget(progress_bar)
            
            self.progress_area.addWidget(progress_widget)
            self.active_downloads[song_id] = {
                'widget': progress_widget,
                'label': song_label,
                'bar': progress_bar
            }
        else:
            # 更新现有的进度条
            progress_info = self.active_downloads[song_id]
            # 只更新进度条值，不更新标签，因为标签会在on_download_finished中更新
            progress_info['bar'].setValue(percentage)

    def on_download_finished(self, song_id_status, success):
        """处理单个下载完成事件"""
        # 解析song_id_status，格式为 "song_id::title (已存在)" 或 "song_id::title"
        if "::" in song_id_status:
            parts = song_id_status.split("::", 1)
            song_id = parts[0]
            display_text = parts[1]
        else:
            song_id = song_id_status
            display_text = song_id_status

        # 使用song_id作为键查找进度条组件
        if song_id in self.active_downloads:
            label = self.active_downloads[song_id]['label']
            
            if "(已存在)" in display_text:
                # 文件已存在
                label.setText(f"✅ {display_text}")
                label.setStyleSheet("color: green; font-weight: bold;")
            elif "没有找到" in display_text:
                # 没有找到
                label.setText(f"❌ {song_id} - {display_text}")
                label.setStyleSheet("color: orange; font-weight: bold;")
            elif success:
                # 下载成功
                label.setText(f"✅ {display_text} - 下载成功")
                label.setStyleSheet("color: green; font-weight: bold;")
            else:
                # 下载失败
                label.setText(f"❌ {display_text}")
                label.setStyleSheet("color: red; font-weight: bold;")
        elif song_id not in self.active_downloads:
            # 如果还没有进度条，则创建一个
            progress_widget = QWidget()
            progress_layout = QVBoxLayout(progress_widget)
            
            # 确定要显示的文本
            if "(已存在)" in display_text:
                final_text = f"✅ {display_text}"
                label_style = "color: green; font-weight: bold;"
            elif "没有找到" in display_text:
                final_text = f"❌ {song_id} - {display_text}"
                label_style = "color: orange; font-weight: bold;"
            elif success:
                final_text = f"✅ {display_text} - 下载成功"
                label_style = "color: green; font-weight: bold;"
            else:
                final_text = f"❌ {display_text}"
                label_style = "color: red; font-weight: bold;"
            
            song_label = QLabel(final_text)
            song_label.setStyleSheet(label_style)
            song_label.setObjectName(f"label_{song_id}")
            
            # 创建一个已完成的进度条
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(100 if success else 0)
            progress_bar.setObjectName(f"progress_{song_id}")
            
            progress_layout.addWidget(song_label)
            progress_layout.addWidget(progress_bar)
            
            self.progress_area.addWidget(progress_widget)
            self.active_downloads[song_id] = {
                'widget': progress_widget,
                'label': song_label,
                'bar': progress_bar
            }

    def on_all_finished(self, success_count, failure_count):
        """全部下载完成"""
        self.thread.quit()
        self.thread.wait()
        self.input_field.setEnabled(True)
        
        # 显示任务结束弹窗
        QMessageBox.information(self, "任务结束", "任务结束！")

    def on_error(self, error_msg):
        """下载过程中发生错误"""
        self.thread.quit()
        self.thread.wait()
        self.input_field.setEnabled(True)
        
        # 显示错误信息
        QMessageBox.critical(self, "下载错误", f"下载过程中发生错误：\n\n{error_msg}")


class WelcomePage(QWidget):
    """欢迎页面"""
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 欢迎文本
        welcome_label = QLabel("欢迎使用音乐下载器")
        welcome_font = QFont()
        welcome_font.setPointSize(18)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #333; margin-bottom: 30px;")
        self.welcome_label = welcome_label
        main_layout.addWidget(welcome_label)

        # Next按钮
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #2196F3;"
            "   color: white;"
            "   border: none;"
            "   padding: 12px 30px;"
            "   border-radius: 6px;"
            "   font-size: 14px;"
            "   font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "   background-color: #0b7dda;"
            "}"
        )
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(self.next_clicked.emit)
        next_btn.setMinimumWidth(100)
        next_btn.setMinimumHeight(40)
        self.next_btn = next_btn
        main_layout.addWidget(next_btn)


class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("下载器")
        self.setGeometry(100, 100, 800, 600)
        self.setup_menu_bar()
        self.setup_central_widget()

    def setup_menu_bar(self):
        menubar = self.menuBar()
        
        # 配置菜单
        config_menu = menubar.addMenu('配置')
        cookie_action = QAction('配置cookie', self)
        # TODO: 实现配置cookie功能
        config_menu.addAction(cookie_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        help_action = QAction('帮助', self)
        # TODO: 实现帮助功能
        help_menu.addAction(help_action)

    def setup_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 初始化欢迎页面
        self.welcome_page = WelcomePage()
        self.service_selection = ServiceSelectionWidget()
        self.download_task_widget = None
        
        layout.addWidget(self.welcome_page)
        
        # 连接信号
        self.welcome_page.next_clicked.connect(self.show_service_selection)
        self.service_selection.service_selected.connect(self.show_download_task)
        self.service_selection.go_back.connect(self.show_welcome_page)
        
        # 设置背景色
        self.setStyleSheet("background-color: white;")

    def show_service_selection(self):
        # 移除当前页面
        for i in range(self.centralWidget().layout().count()):
            widget = self.centralWidget().layout().itemAt(i).widget()
            if widget:
                widget.hide()
        
        # 显示服务选择页面
        self.service_selection.show()
        self.centralWidget().layout().addWidget(self.service_selection)
        self.service_selection.start_animation()

    def show_download_task(self, service_type):
        # 移除当前页面
        for i in range(self.centralWidget().layout().count()):
            widget = self.centralWidget().layout().itemAt(i).widget()
            if widget:
                widget.hide()
        
        # 创建新的下载任务页面
        self.download_task_widget = DownloadTaskWidget(service_type)
        self.centralWidget().layout().addWidget(self.download_task_widget)
        
        # 连接返回信号
        self.download_task_widget.go_back.connect(self.show_service_selection)

    def show_welcome_page(self):
        # 移除当前页面
        for i in range(self.centralWidget().layout().count()):
            widget = self.centralWidget().layout().itemAt(i).widget()
            if widget:
                widget.hide()
        
        # 显示欢迎页面
        self.welcome_page.show()
        self.centralWidget().layout().addWidget(self.welcome_page)


def main():
    app = QApplication(sys.argv)
    
    # 显示协议弹窗
    agreement_dialog = AgreementDialog()
    if agreement_dialog.exec() == QDialog.DialogCode.Accepted:
        # 如果同意，显示主窗口
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # 如果不同意，退出程序
        sys.exit(0)


if __name__ == "__main__":
    main()