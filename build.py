#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动化打包脚本
功能：
1. 清理之前的打包产物
2. 清理Python缓存文件
3. 清除开发配置文件
4. 执行PyInstaller打包
5. 输出打包结果和文件位置
"""

import os
import shutil
import subprocess
import sys
import glob
from pathlib import Path


def clean_build_artifacts():
    """清理之前的打包产物"""
    print("🧹 开始清理之前的打包产物...")
    
    # 删除build目录
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("✅ 已删除 build/ 目录")
    
    # 删除dist目录
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("✅ 已删除 dist/ 目录")
        
    # 删除其他.spec文件（保留music_downloader.spec）
    spec_files = glob.glob('./*.spec')
    for spec_file in spec_files:
        if os.path.basename(spec_file) != 'music_downloader.spec':
            os.remove(spec_file)
            print(f"✅ 已删除 {spec_file} 文件")


def clean_python_cache():
    """清理Python缓存文件"""
    print("\n🗑️ 开始清理Python缓存文件...")
    
    # 删除所有__pycache__目录
    for pycache_dir in Path('.').rglob('__pycache__'):
        try:
            shutil.rmtree(pycache_dir)
            print(f"✅ 已删除 {pycache_dir} 目录")
        except Exception as e:
            print(f"⚠️ 删除 {pycache_dir} 时出错: {e}")
    
    # 删除所有.pyc和.pyo文件
    for py_file in Path('.').rglob('*.py[co]'):
        try:
            py_file.unlink()
            print(f"✅ 已删除 {py_file} 文件")
        except Exception as e:
            print(f"⚠️ 删除 {py_file} 时出错: {e}")


def clean_dev_config():
    """清理开发配置文件"""
    print("\n🔧 开始清理开发配置文件...")
    
    # 查找并删除可能包含敏感信息的文件
    dev_files = [
        'cookies_y.qq.com.txt',  # 从项目结构中发现的cookie文件
        'cookies.txt',
        'session.json',
        '.env',
        '*.log',
        'logs/*'
    ]
    
    for pattern in dev_files:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    print(f"✅ 已删除 {file_path} 文件")
                except Exception as e:
                    print(f"⚠️ 删除 {file_path} 时出错: {e}")


def run_pyinstaller():
    """执行PyInstaller打包"""
    print("\n📦 开始执行PyInstaller打包...")
    
    try:
        # 执行PyInstaller命令
        cmd = [sys.executable, '-m', 'PyInstaller', 'music_downloader.spec']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("✅ PyInstaller打包成功!")
        print("STDOUT:", result.stdout[-500:])  # 只打印最后500个字符避免输出过多
        
        return True
    except subprocess.CalledProcessError as e:
        print("❌ PyInstaller打包失败!")
        print("STDERR:", e.stderr)
        return False


def optimize_size():
    """尝试优化打包体积"""
    print("\n🔬 尝试优化打包体积...")
    
    # 这里可以添加更多体积优化逻辑
    # 例如，删除不必要的语言文件、字体等
    print("💡 体积优化建议:")
    print("   - 检查spec文件中的excludes列表是否包含了不必要的模块")
    print("   - 考虑使用UPX压缩（已在spec文件中禁用）")
    print("   - 如果不需要多语言支持，可以排除Qt的语言文件")


def show_result():
    """显示打包结果和文件位置"""
    print("\n📋 打包结果:")
    
    # 检查可执行文件是否存在
    exe_path = './dist/music-downloader.exe'  # 单文件模式的路径
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        size_mb = size / (1024 * 1024)
        print(f"✅ 可执行文件已生成: {os.path.abspath(exe_path)}")
        print(f"📊 文件大小: {size_mb:.2f} MB")
        print(f"🎯 文件路径: {exe_path}")
        return True
    else:
        print("❌ 未找到可执行文件，请检查打包过程是否有错误")
        return False


def main():
    """主函数"""
    print("🎵 音乐下载器打包工具")
    print("=" * 50)
    
    # 确认是否继续
    # response = input("是否继续执行打包? (y/N): ")
    # if response.lower() not in ['y', 'yes']:
    #     print("❌ 打包已取消")
    #     return
    
    # 执行打包流程
    clean_build_artifacts()
    clean_python_cache()
    clean_dev_config()
    optimize_size()
    
    success = run_pyinstaller()
    if success:
        show_result()
        print("\n🎉 打包完成！")
    else:
        print("\n💥 打包失败，请检查错误信息")


if __name__ == '__main__':
    main()