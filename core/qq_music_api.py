import re
import json
import requests
from config.settings import API_CONFIG

class QQMusicAPI:
    """QQ音乐API接口类"""
    
    @staticmethod
    def get_playlist_song_ids(playlist_url):
        """
        从QQ音乐歌单提取所有歌曲ID
        Args:
            playlist_url: 歌单URL
        Returns:
            list: 歌曲ID列表
        """
        # 解析歌单ID
        match = re.search(r'/playlist/(\d+)', playlist_url)
        if not match:
            print("❌ 无法解析歌单ID")
            return []

        disstid = match.group(1)
        print(f"🔍 解析到歌单ID: {disstid}")

        try:
            # 发送API请求
            response = requests.get(
                API_CONFIG['playlist_api'],
                params={
                    "type": 1,
                    "json": 1,
                    "utf8": 1,
                    "disstid": disstid,
                    "format": "json"
                },
                headers=API_CONFIG['headers'],
                timeout=10
            )
            
            # 处理JSONP响应
            json_str = re.search(r'\{.*\}', response.text, re.S)
            if not json_str:
                print("❌ 接口被拦截或返回异常")
                print(f"响应预览: {response.text[:200]}")
                return []

            data = json.loads(json_str.group())
            
            # 提取歌曲列表
            song_list = data["cdlist"][0]["songlist"]
            song_ids = [song["songmid"] for song in song_list]
            
            print(f"✅ 成功获取 {len(song_ids)} 首歌曲")
            return song_ids

        except Exception as e:
            print(f"❌ 获取歌单失败: {e}")
            return []


# TODO: 其他音乐平台API可以在这里扩展
# class NetEaseMusicAPI:
#     """网易云音乐API"""
#     pass

# class KuGouMusicAPI:
#     """酷狗音乐API"""
#     pass