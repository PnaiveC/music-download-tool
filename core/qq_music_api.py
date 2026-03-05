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
            playlist_url: 歌单URL或歌单ID
        Returns:
            list: 歌曲ID列表
        """
        # 检查输入是URL还是ID
        if playlist_url.isdigit():
            # 如果是纯数字，认为是歌单ID
            disstid = playlist_url
            print(f"🔍 解析到歌单ID: {disstid}")
        else:
            # 如果是URL，从中提取ID
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
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"❌ API请求失败，状态码: {response.status_code}")
                return []
            
            # 处理JSONP响应
            json_str = re.search(r'\{.*\}', response.text, re.S)
            if not json_str:
                print("❌ 接口被拦截或返回异常")
                print(f"响应预览: {response.text[:200]}")
                return []

            data = json.loads(json_str.group())
            
            # 检查返回的数据是否包含错误
            if "code" in data and data["code"] != 0:
                print(f"❌ API返回错误: {data.get('code', 'unknown')}")
                return []
            
            # 检查cdlist是否存在
            if "cdlist" not in data or not data["cdlist"]:
                print("❌ 歌单数据为空或不存在")
                return []
                
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