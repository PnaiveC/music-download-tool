#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐下载器主程序
支持QQ音乐单曲和歌单下载，具备多线程、日志统计等功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.downloaders.multithread_downloader import MultithreadDownloader
from core.api.qq_music_api import QQMusicAPI
from utils.logger import print_final_statistics

def get_user_choice():
    """获取用户选择：歌单下载还是指定歌曲下载"""
    while True:
        print("\n🎵 音乐下载器")
        print("=" * 30)
        print("请选择下载方式:")
        print("1. 歌单下载")
        print("2. 指定歌曲下载")
        print("3. 退出程序")
        
        try:
            choice = input("\n请输入选项 (1/2/3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 程序退出")
            sys.exit(0)
        
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("❌ 无效选项，请重新输入")

def get_playlist_url():
    """获取歌单URL"""
    print("\n📋 歌单下载模式")
    print("-" * 20)
    print("请输入QQ音乐歌单URL")
    print("示例: https://y.qq.com/n/ryqq/playlist/123456")
    print("(直接回车使用默认歌单)")
    
    try:
        url = input("\n歌单URL: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n👋 程序退出")
        sys.exit(0)
    
    if not url:
        # 使用默认歌单
        url = "https://y.qq.com/n/ryqq_v2/playlist/9630613589"
        print(f"使用默认歌单: {url}")
    
    return url

def get_song_ids():
    """获取歌曲ID列表"""
    print("\n🎵 指定歌曲下载模式")
    print("-" * 25)
    print("请输入歌曲ID，支持多个ID")
    print("示例: 003aAYrm3GE0Ac 003uEbEr0jcW7c")
    print("输入 'q' 开始下载")
    
    song_ids = []
    while True:
        try:
            song_id = input("歌曲ID: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 程序退出")
            sys.exit(0)
        
        if song_id.lower() == 'q':
            if song_ids:
                break
            else:
                print("⚠️  请至少输入一个歌曲ID")
                continue
        
        if song_id:
            song_ids.append(song_id)
            print(f"✅ 已添加: {song_id} (总计: {len(song_ids)}个)")
        else:
            print("⚠️  输入不能为空")
    
    return song_ids

def main():
    """主程序入口"""
    print("🎵 音乐下载器启动中...")
    
    while True:
        try:
            choice = get_user_choice()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 程序退出")
            break
            
        if choice == '3':
            print("👋 程序退出")
            break
            
        elif choice == '1':
            # 歌单下载
            try:
                playlist_url = get_playlist_url()
                print(f"🔍 正在获取歌单: {playlist_url}")
                
                # 获取歌单歌曲ID
                song_ids = QQMusicAPI.get_playlist_song_ids(playlist_url)
                
                if song_ids:
                    print(f"✅ 获取到 {len(song_ids)} 首歌曲，开始下载...")
                    downloader = MultithreadDownloader()
                    downloader.download_files(song_ids)
                else:
                    print("❌ 未能获取歌单歌曲，请检查链接是否有效")
                    continue
            except (EOFError, KeyboardInterrupt):
                print("\n\n👋 程序退出")
                break
                
        elif choice == '2':
            # 指定歌曲下载
            try:
                song_ids = get_song_ids()
                if song_ids:
                    print(f"✅ 准备下载 {len(song_ids)} 首歌曲...")
                    downloader = MultithreadDownloader()
                    downloader.download_files(song_ids)
                else:
                    print("❌ 未获取到有效的歌曲ID")
                    continue
            except (EOFError, KeyboardInterrupt):
                print("\n\n👋 程序退出")
                break
        
        # 打印最终统计信息
        print_final_statistics()
        
        # 询问是否继续
        try:
            continue_choice = input("\n是否继续下载? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("👋 程序退出")
                break
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 程序退出")
            break

if __name__ == "__main__":
    main()