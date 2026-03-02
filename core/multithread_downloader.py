import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.settings import THREAD_CONFIG
from utils.logger import log_failure, update_stats
from core.downloader import MusicDownloader

class MultithreadDownloader:
    """多线程下载器 - 支持并发下载"""
    
    def __init__(self, max_workers=None):
        # 智能设置线程数：根据CPU核心数和网络I/O能力优化
        if max_workers is None:
            cpu_count = multiprocessing.cpu_count()
            # 对于I/O密集型任务，线程数可以设为CPU核心数的2-4倍
            self.max_workers = min(cpu_count * 3, THREAD_CONFIG['max_workers'])
        else:
            self.max_workers = min(max_workers, 10)  # 限制最大线程数为10
        
        self.downloader = MusicDownloader()
        print(f"🔧 初始化多线程下载器，线程数: {self.max_workers}")
    
    def download_files(self, file_list, max_retries=None):
        """
        多线程下载文件列表
        Args:
            file_list: 文件ID或URL列表
            max_retries: 最大重试次数
        """
        if not file_list:
            print("📋 文件列表为空")
            return
        
        # 去重处理 - 确保同一首歌只下载一次
        unique_files = list(dict.fromkeys(file_list))  # 保持顺序的去重
        duplicates_removed = len(file_list) - len(unique_files)
        
        if duplicates_removed > 0:
            print(f"🔍 检测到 {duplicates_removed} 个重复任务，已自动去重")
        
        print(f"🚀 开始多线程下载 {len(unique_files)} 个文件...")
        
        # 重置统计计数器（避免累积之前的统计）
        global success_count, failure_count
        from utils.logger import success_count, failure_count
        initial_success = success_count
        initial_failure = failure_count
        
        # 记录开始时间用于性能统计
        start_time = time.time()
        
        # 使用线程池执行下载任务
        with ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="DownloadWorker"
        ) as executor:
            # 提交所有下载任务
            future_to_file = {
                executor.submit(
                    self._download_with_timing, 
                    file_id, 
                    max_retries
                ): file_id for file_id in unique_files
            }
            
            # 处理完成的任务
            completed = 0
            total = len(unique_files)
            successful = 0
            failed = 0
            
            # 按完成顺序处理结果
            for future in as_completed(future_to_file, timeout=THREAD_CONFIG['timeout']):
                file_id = future_to_file[future]
                completed += 1
                
                try:
                    result, download_time = future.result(timeout=THREAD_CONFIG['task_timeout'])
                    status = "✅ 成功" if result else "❌ 失败"
                    if result:
                        successful += 1
                        if download_time:
                            print(f"📊 进度: {completed}/{total} - {file_id}: {status} (耗时: {download_time:.1f}s)")
                        else:
                            print(f"📊 进度: {completed}/{total} - {file_id}: {status}")
                    else:
                        failed += 1
                        print(f"📊 进度: {completed}/{total} - {file_id}: {status}")
                        
                except Exception as e:
                    failed += 1
                    print(f"📊 进度: {completed}/{total} - {file_id}: ⚠️ 异常 - {str(e)[:50]}...")
                    log_failure("multithread_download", str(e), file_id)
            
            # 更新最终统计（只统计本次下载的结果）
            update_stats(True, successful)
            update_stats(False, failed)
            
            # 计算总体性能
            end_time = time.time()
            total_time = end_time - start_time
            avg_speed = len(unique_files) / total_time if total_time > 0 else 0
            
            print(f"\n📈 本次下载统计:")
            print(f"   总任务: {total}")
            print(f"   成功: {successful}")
            print(f"   失败: {failed}")
            print(f"   总耗时: {total_time:.1f}秒")
            print(f"   平均速度: {avg_speed:.2f} 任务/秒")
            if duplicates_removed > 0:
                print(f"   ⚠️  已去除重复任务: {duplicates_removed}")

    def _download_with_timing(self, file_id, max_retries):
        """
        带时间统计的下载方法
        返回: (下载结果, 下载耗时)
        """
        start_time = time.time()
        try:
            result = self.downloader.download_single_file(file_id, max_retries=max_retries)
            end_time = time.time()
            download_time = end_time - start_time
            return result, download_time
        except Exception as e:
            end_time = time.time()
            download_time = end_time - start_time
            raise e


# TODO: GUI集成 - 添加进度回调接口
# TODO: GUI集成 - 添加暂停/恢复功能
# TODO: GUI集成 - 添加任务队列管理