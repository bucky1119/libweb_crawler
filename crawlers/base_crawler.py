# crawlers/base_crawler.py
from abc import ABC, abstractmethod
from common import ArticleContent
from typing import Any, Dict, List

class AbstractCrawler(ABC):
    def __init__(self, config: dict):
        self.config = config
    @abstractmethod
    async def crawl(self) -> List[ArticleContent]:
        """
        执行爬取和数据解析任务，返回 ArticleContent 对象
        """
        raise NotImplementedError("子类必须实现 crawl 方法")