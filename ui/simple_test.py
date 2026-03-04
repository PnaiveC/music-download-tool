import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.gui import AgreementDialog, MainWindow

def test_components():
    """Test that GUI components can be instantiated without errors"""
    app = QApplication(sys.argv)
    
    try:
        print("Testing AgreementDialog creation...")
        dialog = AgreementDialog()
        print("✓ AgreementDialog created successfully")
        
        print("Testing MainWindow creation...")
        window = MainWindow()
        print("✓ MainWindow created successfully")
        
        print("\nAll components created successfully!")
        print("Note: This does not launch the full application, just verifies component instantiation.")
        
        # Show a message confirming successful initialization
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("测试成功")
        msg.setText("GUI组件创建成功！")
        msg.setDetailedText("所有GUI组件都可以正确初始化。要运行完整应用，请执行: python -m ui.gui")
        msg.exec()
        
        return True
        
    except Exception as e:
        print(f"Error creating components: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_components()