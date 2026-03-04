import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QScrollArea, QLineEdit, QProgressBar, QFrame,
    QMenuBar, QMenu, QSizePolicy, QToolButton, QDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QSequentialAnimationGroup, QPoint, QParallelAnimationGroup
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

        placeholder_text = "请输入歌单 ID" if self.service_type == "playlist" else "请输入歌曲 ID"
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder_text)
        self.input_field.setMinimumWidth(250)
        input_layout.addWidget(self.input_field)

        start_btn = QPushButton("开始下载")
        start_btn.clicked.connect(self.start_download)
        input_layout.addWidget(start_btn)

        main_layout.addLayout(input_layout)

        # 进度显示区域
        self.progress_area = QVBoxLayout()
        self.progress_area.setSpacing(10)
        main_layout.addLayout(self.progress_area)

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
        # TODO: 实现下载逻辑，连接到核心下载模块
        input_value = self.input_field.text().strip()
        if not input_value:
            # 可以在这里添加提示
            return

        # 显示下载进度（模拟）
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        
        song_label = QLabel(f"正在下载: {input_value}")
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        
        progress_layout.addWidget(song_label)
        progress_layout.addWidget(progress_bar)
        
        self.progress_area.addWidget(progress_widget)

        # 模拟下载进度
        timer = QTimer()
        progress_value = 0
        
        def update_progress():
            nonlocal progress_value
            progress_value += 5
            if progress_value <= 100:
                progress_bar.setValue(progress_value)
            else:
                timer.stop()
                # 下载完成后在进度条右下角显示成功消息
                self.show_success_message(input_value)
        
        timer.timeout.connect(update_progress)
        timer.start(100)

    def show_success_message(self, song_id):
        """在进度条右下角显示成功消息"""
        # 创建成功消息标签
        success_label = QLabel(f"{song_id} - 下载成功")
        success_label.setStyleSheet("color: green; font-weight: bold;")
        success_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 添加到进度区域
        self.progress_area.addWidget(success_label)


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