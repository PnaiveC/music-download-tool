# -*- coding: utf-8 -*-
"""
音乐下载器GUI主入口
重构为模块化结构，使用分离的组件
"""

import sys
import os
# 添加项目根目录到Python路径，以便正确导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

from ui.widgets.dialogs import AgreementDialog
from ui.widgets.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    
    # 显示协议弹窗
    agreement_dialog = AgreementDialog()
    if agreement_dialog.exec() == agreement_dialog.DialogCode.Accepted:
        # 如果同意，显示主窗口
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # 如果不同意，退出程序
        sys.exit(0)


if __name__ == "__main__":
    main()