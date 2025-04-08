# tests/test_crawler_common.py

import asyncio
import unittest
from typing import List
from common import ArticleContent
from crawlers.base_crawler import AbstractCrawler
from config import get_website_configs
import sys
import re


def get_crawler_config_by_name(name: str) -> dict:
    """
    从配置中查找指定名称的爬虫配置
    """
    configs = get_website_configs()
    print(configs)
    for cfg in configs:
        if cfg.get("name") == name:
            return cfg
    raise ValueError(f"未找到名称为 {name} 的爬虫配置")

async def test_crawler(config: dict):
    """
    公共测试函数：根据传入配置初始化爬虫并测试其 crawl 方法，
    该方法返回 ArticleContent 列表，验证每个元素的有效性。
    """
    # 根据配置中的 crawler_class 获取对应爬虫类并实例化
    crawler: AbstractCrawler = config['crawler_class'](config)
    print(crawler)
    # 执行爬虫任务，返回文章列表
    article_list: List[ArticleContent] = await crawler.crawl()
    print(article_list)
    # 验证返回结果为列表且不为空
    assert isinstance(article_list, list), f"{config.get('name')} 返回值不是列表"
    assert len(article_list) > 0, f"{config.get('name')} 返回的文章列表为空"
    
    # 对每个 ArticleContent 对象进行断言检查
    for article in article_list:
        assert isinstance(article, ArticleContent), "列表中的元素不是 ArticleContent 对象"
        assert article.title, f"{config.get('name')} 中某篇文章的标题为空"
        assert article.link_url, f"{config.get('name')} 中某篇文章的链接为空"
    
    print(f"测试成功：{config.get('name')} 返回 {len(article_list)} 篇文章")

# # 使用 unittest 进行集成测试
# class TestCrawlerCommon(unittest.IsolatedAsyncioTestCase):
#     async def test_specific_crawler(self):
#         # 修改为你想测试的爬虫名称，比如 "网站1"
#         crawler_name = "网站61"
#         config = get_crawler_config_by_name(crawler_name)
#         await test_crawler(config)

#     async def test_all_crawlers(self):
#         # 依次测试所有配置的爬虫
#         configs = get_website_configs()
#         for config in configs:
#             with self.subTest(crawler=config.get("name")):
#                 await test_crawler(config)

if __name__ == "__main__":
    # 直接指定一个爬虫名称
    crawler_name = "网站4"
    config = get_crawler_config_by_name(crawler_name)
    print(config)
    asyncio.run(test_crawler(config))


# if __name__ == "__main__":
#     # 如果直接运行该测试模块，可以选择执行单个爬虫或所有爬虫测试
#     import sys

#     if len(sys.argv) > 1:
#         # 命令行参数中传入爬虫名称，如: python test_crawler_common.py "网站1"
#         crawler_name = sys.argv.pop()
#         config = get_crawler_config_by_name(crawler_name)
#         asyncio.run(test_crawler(config))
#     else:
#         unittest.main()
