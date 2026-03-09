# -*- coding: utf-8 -*-
"""
组件模块，包含各种UI组件
"""

import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QScrollArea, QLineEdit, QProgressBar, QFrame,
    QToolButton, QListWidget, QListWidgetItem,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QSequentialAnimationGroup, QPoint, QParallelAnimationGroup, QThread, QObject, pyqtSlot
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QColor


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
        from .threads import DownloadWorker
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