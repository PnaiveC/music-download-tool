# -*- coding: utf-8 -*-
"""
主窗口模块，负责管理应用程序的主要界面
"""

import sys
import os
# 添加项目根目录到Python路径，以便正确导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QScrollArea, QLineEdit, QProgressBar, QFrame,
    QMenuBar, QMenu, QSizePolicy, QToolButton, QDialog, QListWidget, QListWidgetItem,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QColor


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
        cookie_action.triggered.connect(self.configure_cookie)
        config_menu.addAction(cookie_action)
        
        # 新增：下载位置配置
        download_location_action = QAction('下载位置', self)
        download_location_action.triggered.connect(self.configure_download_location)
        config_menu.addAction(download_location_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        help_action = QAction('帮助', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def configure_cookie(self):
        """配置cookie文件"""
        from .dialogs import CookieConfigDialog
        dialog = CookieConfigDialog(self)
        result = dialog.exec()
        if result == QMessageBox.StandardButton.Yes:
            # 获取cookie文件路径
            from config.settings import DOWNLOAD_CONFIG
            cookie_path = DOWNLOAD_CONFIG['cookie_path']
            
            # 如果文件不存在则创建
            if not os.path.exists(cookie_path):
                os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
                with open(cookie_path, 'w', encoding='utf-8') as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    f.write("# 请在此处粘贴您的Cookie信息\n")
                    f.write("# 示例格式:\n")
                    f.write("# .y.qq.com	TRUE	/	TRUE	2147483647	wxuin	yours123\n")
            
            # 使用系统默认编辑器打开文件
            try:
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f'open "{cookie_path}"')
                elif sys.platform.startswith('win'):   # Windows
                    os.startfile(cookie_path)
                elif sys.platform.startswith('linux'): # Linux
                    os.system(f'xdg-open "{cookie_path}"')
            except Exception as e:
                # 如果系统命令失败，使用Qt内置方式打开
                QMessageBox.warning(self, "提示", f"无法自动打开文件，路径为: {cookie_path}\n请手动编辑此文件。")

    def configure_download_location(self):
        """配置下载位置"""
        from config.settings import DOWNLOAD_CONFIG, update_download_location
        
        # 获取当前下载位置
        current_location = DOWNLOAD_CONFIG.get('download_location', DOWNLOAD_CONFIG['download_dir'])
        
        # 弹出文件夹选择对话框
        selected_dir = QFileDialog.getExistingDirectory(
            self, 
            "选择下载位置", 
            current_location,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if selected_dir:
            # 尝试更新下载位置
            if update_download_location(selected_dir):
                QMessageBox.information(self, "成功", f"下载位置已更新为:\n{selected_dir}")
            else:
                QMessageBox.critical(self, "错误", "所选目录不可写或不存在，请选择一个有效的目录！")

    def show_help(self):
        """显示帮助信息"""
        from .dialogs import HelpDialog
        help_dialog = HelpDialog()
        help_dialog.exec()

    def setup_central_widget(self):
        from .components import WelcomePage, ServiceSelectionWidget
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
        # 验证下载位置是否有效
        from config.settings import is_download_location_valid
        if not is_download_location_valid():
            QMessageBox.warning(self, "下载位置未配置", "请参阅帮助 配置有效的下载位置")
            return
        
        # 移除当前页面
        for i in range(self.centralWidget().layout().count()):
            widget = self.centralWidget().layout().itemAt(i).widget()
            if widget:
                widget.hide()
        
        # 创建新的下载任务页面
        from .components import DownloadTaskWidget
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