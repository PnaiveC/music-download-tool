import os
import logging
from datetime import datetime
from collections import defaultdict
from config.settings import LOG_CONFIG

# 确保日志目录存在
log_dir = LOG_CONFIG['log_dir']
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 创建按日期命名的日志文件
log_filename = os.path.join(log_dir, f"download_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=getattr(logging, LOG_CONFIG['log_level']),
    format=LOG_CONFIG['log_format'],
    encoding='utf-8'
)

# 失败统计字典：{错误类型: {次数: int, 最后发生时间: str}}
failure_stats = defaultdict(lambda: {"count": 0, "last_time": ""})

# 下载统计
success_count = 0
failure_count = 0

def reset_stats():
    """重置统计计数器"""
    global success_count, failure_count
    success_count = 0
    failure_count = 0

def log_failure(operation, error_msg, url=""):
    """
    记录失败信息并统计同类失败次数
    只记录失败本身和次数，合并相同类型的错误
    """
    # 创建唯一的失败标识（按操作类型和错误信息分类）
    # 使用完整的错误信息，但限制长度避免过长
    error_key = str(error_msg)[:200] if len(str(error_msg)) > 200 else str(error_msg)
    failure_key = f"{operation}_{error_key}"
    
    # 更新统计信息
    failure_stats[failure_key]["count"] += 1
    failure_stats[failure_key]["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 记录到日志文件（详细信息）
    logging.error(f"操作: {operation} | URL: {url} | 错误: {error_msg} | 次数: {failure_stats[failure_key]['count']}")

def update_stats(success=True, count=1):
    """更新下载成功/失败统计"""
    global success_count, failure_count
    if success:
        success_count += count
    else:
        failure_count += count

def add_download_delay(min_delay=1, max_delay=3):
    """添加随机下载延迟，减少被封风险"""
    import random
    import time
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def print_final_statistics():
    """打印下载统计和失败分析"""
    print("\n" + "="*50)
    print("📊 下载任务完成统计")
    print("="*50)
    print(f"✅ 成功下载: {success_count}")
    print(f"❌ 下载失败: {failure_count}")
    print(f"📈 总任务数: {success_count + failure_count}")
    
    if success_count + failure_count > 0:
        success_rate = (success_count / (success_count + failure_count)) * 100
        print(f"🎯 成功率: {success_rate:.1f}%")
    
    if failure_count > 0:
        print("\n🔍 失败详情分析:")
        print("-" * 40)
        # 按失败次数排序显示
        for failure_key, stats in sorted(failure_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            operation, error = failure_key.split("_", 1)
            print(f"🔧 操作: {operation}")
            print(f"⚠️  错误: {error[:50]}{'...' if len(error) > 50 else ''}")
            print(f"🔢 次数: {stats['count']}")
            print(f"🕐 最后发生: {stats['last_time']}")
            print("-" * 40)
    
    print("="*50)