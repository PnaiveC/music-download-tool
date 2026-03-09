# -*- coding: utf-8 -*-
"""
对话框模块，包含各种弹窗对话框
"""

import sys
import os
from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QTextEdit, QScrollArea, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QWidget, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HelpDialog(QDialog):
    """帮助弹窗"""
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("帮助")
        self.setMinimumSize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("使用帮助")
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
        <p><strong>欢迎使用音乐下载器</strong></p>
        <br>
        <p><strong>功能说明：</strong></p>
        <ul>
          <li>支持QQ音乐单曲下载：输入歌曲ID即可下载</li>
          <li>支持QQ音乐歌单下载：输入歌单链接批量下载</li>
          <li>多线程并发下载：最多5个线程同时工作，提高下载效率</li>
          <li>实时进度显示：显示每个下载任务的进度和状态</li>
          <li>智能去重：自动过滤重复的下载任务</li>
          <li>断点续传：已存在的文件自动跳过，避免重复下载</li>
        </ul>

        <p><strong>使用步骤：</strong></p>
        <ol>
          <li>配置Cookie：点击"配置"菜单->"配置cookie"，确保Cookie文件有效</li>
          <li>配置下载位置：点击"配置"菜单->"下载位置"，选择有效的下载目录</li>
          <li>选择服务：点击"下载歌单内所有歌曲"或"下载我需要的歌曲"</li>
          <li>输入信息：输入歌单链接或歌曲ID（多个ID用空格分隔）</li>
          <li>开始下载：点击"开始下载"按钮，等待下载完成</li>
        </ol>

        <p><strong>注意事项：</strong></p>
        <ul>
          <li>请确保Cookie文件有效，否则可能无法下载</li>
          <li>请确保下载位置有效且具有写入权限</li>
          <li>输入歌曲ID时，请确保格式正确（如：004R7qfh1ALctJ）</li>
          <li>下载大量音乐时，请确保有足够的存储空间</li>
          <li>请遵守相关法律法规，仅用于个人学习和备份</li>
          <li>如果遇到下载失败，请检查网络连接和Cookie有效性</li>
        </ul>

        <p><strong>常见问题：</strong></p>
        <ul>
          <li>Q: 为什么有些歌曲下载失败？</li>
          <li>A: 可能由于版权原因或Cookie过期导致，尝试更新Cookie后重试</li>
          <li>Q: 如何获取歌曲ID？</li>
          <li>A: 在QQ音乐网站播放歌曲时，地址栏URL中通常包含歌曲ID</li>
          <li>Q: 下载的音乐保存在哪里？</li>
          <li>A: 默认保存在配置文件中指定的目录，默认为 'C:\\Users\\Prologue\\Music'</li>
          <li>Q: 为什么点击下载时提示配置下载位置？</li>
          <li>A: 请检查是否设置了有效的下载位置，可通过"配置"->"下载位置"进行设置</li>
        </ul>

        <p><strong>技术支持：</strong></p>
        <p>如遇问题，请查看项目README文档或联系开发者。</p>
        </div>
        """)
        content_layout.addWidget(content_text)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        main_layout.addWidget(content_area)

        # 确定按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_btn = QPushButton("确定")
        ok_btn.setStyleSheet(
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
        ok_btn.clicked.connect(self.accept)

        button_layout.addWidget(ok_btn)
        main_layout.addLayout(button_layout)


class CookieConfigDialog(QMessageBox):
    """Cookie配置提示对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置Cookie")
        self.setText("Cookie文件是你通过QQ音乐下载音乐的凭证<br/>若没有或已过期，您需前往官网获取。")
        self.setInformativeText("是否现在配置Cookie文件？")
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.Yes)


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
          <li>使用过程中请确保下载位置有效且具有写入权限</li>
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