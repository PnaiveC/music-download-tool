import sys
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.gui import AgreementDialog, WelcomePage, ServiceSelectionWidget, DownloadTaskWidget, MainWindow


class TestAgreementDialog(unittest.TestCase):
    """测试协议对话框"""
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_dialog_creation(self):
        dialog = AgreementDialog()
        self.assertIsNotNone(dialog)
        self.assertEqual(dialog.windowTitle(), "使用须知")
    
    def test_agree_button(self):
        dialog = AgreementDialog()
        # 模拟点击同意按钮
        for child in dialog.findChildren(QPushButton):
            if child.text() == "我已知晓并同意":
                agree_btn = child
                break
        else:
            self.fail("未找到同意按钮")
        
        agree_btn.click()
        # 应该返回Accepted
        self.assertEqual(dialog.result(), dialog.DialogCode.Accepted)
    
    def test_cancel_button(self):
        dialog = AgreementDialog()
        # 模拟点击取消按钮
        for child in dialog.findChildren(QPushButton):
            if child.text() == "退出":
                cancel_btn = child
                break
        else:
            self.fail("未找到取消按钮")
        
        cancel_btn.click()
        # 应该返回Rejected
        self.assertEqual(dialog.result(), dialog.DialogCode.Rejected)


class TestWelcomePage(unittest.TestCase):
    """测试欢迎页面"""
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_welcome_page_creation(self):
        page = WelcomePage()
        self.assertIsNotNone(page)
        self.assertEqual(page.findChild(type(page.welcome_label)).text(), "欢迎使用音乐下载器")


class TestServiceSelectionWidget(unittest.TestCase):
    """测试服务选择页面"""
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_service_selection_creation(self):
        widget = ServiceSelectionWidget()
        self.assertIsNotNone(widget)
        self.assertIsNotNone(widget.playlist_btn)
        self.assertIsNotNone(widget.song_btn)


class TestDownloadTaskWidget(unittest.TestCase):
    """测试下载任务页面"""
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_playlist_download_creation(self):
        widget = DownloadTaskWidget("playlist")
        self.assertIsNotNone(widget)
        self.assertIn("歌单", widget.top_label.text())
    
    def test_song_download_creation(self):
        widget = DownloadTaskWidget("song")
        self.assertIsNotNone(widget)
        self.assertIn("歌曲", widget.top_label.text())


class TestMainWindow(unittest.TestCase):
    """测试主窗口"""
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_main_window_creation(self):
        window = MainWindow()
        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "下载器")


def run_tests():
    """运行所有测试"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()