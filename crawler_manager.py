import asyncio
from typing import Any, Dict, List
from crawlers.base_crawler import AbstractCrawler
from config import get_website_configs
from storage.abstract_store_impl import StoreFactory
from log import get_logger
from common import ArticleContent
import time
from monitoring import CURRENT_TASKS, TASK_SUCCESS_COUNT, TASK_FAILURE_COUNT, TASK_EXECUTION_TIME

logger = get_logger("CrawlerManager")

class CrawlerManager:
    def __init__(self):
        # 从配置中加载所有网站的配置
        self.website_configs = get_website_configs()

    async def crawl_website(self, config: Dict):
        # 根据配置选择合适的爬虫实例，此处假设所有爬虫均继承了AbstractCrawler
        crawler: AbstractCrawler = config['crawler_class'](config)
        CURRENT_TASKS.inc()  # 任务开始，计数器 +1
        start_time = time.time()
        try:
            logger.info(f"开始爬取: {config['name']}")
            # step1 遍历数据并解析存储到数据容器中
            article_content_list: List[ArticleContent] = await crawler.crawl()
            print(len(article_content_list))
            # step2 将爬取到的数据存入数据库，可根据需要选择存储方式
            # 使用工厂模式获取 CSV 和数据库的存储实例
            csv_store = StoreFactory.get_store("csv")
            db_store = StoreFactory.get_store("db")
            for data_item in article_content_list:
                if data_item.title and data_item.link_url:
                    try:
                        # 存储到 csv 文件
                        await csv_store.save(data_item)
                        # 存储到数据库
                        await db_store.save(data_item)
                    except Exception as e:
                        logger.error(f"Error saving data item: {data_item}. Error: {e}")
                else:
                    # 记录一个警告日志，说明跳过了这个 data_item
                    logger.info(f"Skipping data item due to missing title or link_url: {data_item}")
            TASK_SUCCESS_COUNT.inc()  # 任务成功，计数器 +1
            logger.info(f"{config['name']} 爬取并存储成功")
        except Exception as e:
            # 异常处理及日志记录
            TASK_FAILURE_COUNT.inc()  # 任务失败，计数器 +1
            print(f"爬虫 {config['name']} 出错: {e}")
            logger.error(f"爬虫 {config['name']} 出错: {e}", exc_info=True)
        finally:
            elapsed = time.time() - start_time
            TASK_EXECUTION_TIME.observe(elapsed)
            CURRENT_TASKS.dec()  # 任务结束，计数器 -1

    async def start_all_tasks(self):
        tasks = [self.crawl_website(config) for config in self.website_configs]
        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # 对结果进行处理或记录错误
        for result in results:
            if isinstance(result, Exception):
                print(f"任务错误: {result}")
                logger.error(f"任务错误: {result}")
