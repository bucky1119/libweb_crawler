from apscheduler.schedulers.asyncio import AsyncIOScheduler
from crawler_manager import CrawlerManager

async def start_scheduler():
    manager = CrawlerManager()
    scheduler = AsyncIOScheduler()
    # 假设每隔10分钟启动一次所有网站的爬虫任务
    # scheduler.add_job(manager.start_all_tasks, 'interval', minutes=10)
    # scheduler.start()
    # 立即执行一次
    await manager.start_all_tasks()
