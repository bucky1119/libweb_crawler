# crawlers/website61_crawler.py
# "name": "网站61",
# "crawler_class": __import__("crawlers.website61_crawler", fromlist=["Website61Crawler"]).Website61Crawler,
# "url": "https://foodtank.com/news/category/food-tank/",
import asyncio
from typing import Any, Dict, List
from crawlers.base_crawler import AbstractCrawler
from common import ArticleContent
from playwright.async_api import async_playwright
from parsel import Selector
from datetime import date
import random

class Website61Crawler(AbstractCrawler):
    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get("url")
        # 其他配置参数，比如请求头、超时设置等可以在此处初始化
        # 是否翻页运行标志
        self.running_state = True
        # 翻页计数器
        self.page_count = 1
        # 限制爬取页数
        self.PAGE_SIZE = 3
    
    def parse_article_content(self, container_selector: Selector) -> ArticleContent:
        """
        数据提取
        :param quote_item:
        :return:
        """
        # 构造 ArticleContent 对象，其他字段可根据需求补充
        article = ArticleContent(
            title=container_selector.xpath('.//h5/a/text()').get(),
            author="",
            link_url=container_selector.xpath('.//h5/a/@href').get(),
            text=container_selector.xpath('.//div[@class="post-content entry-content small"]/p/text()').get(),
            nation="",# 无
            post_agency="非政府组织",# 非政府组织
            article_date=str(date.today().isoformat()),  # 使用当前日期，可根据需求调整
            # 以下默认字段，暂时不需要调整
            info_type="T0",
            domain="F0",
            subject="AG0",
        )
        return article

    async def crawl(self) -> List[ArticleContent]:
        """
        异步爬取页面内容，并解析为 ArticleContent 对象
        发送请求获取数据,储存到symbol_data_list中
        :param max_total_count:
        :return:
        """
        article_data_list: List[ArticleContent] = []
        while self.running_state and self.page_count <= self.PAGE_SIZE:
            html = await self.fetch_page()
            selector = Selector(text=html)
            container_list = selector.xpath('//*[@id="content-container"]/div[4]/div/section/div')
            for container in container_list:
                parsed_content: ArticleContent = self.parse_article_content(container)
                article_data_list.append(parsed_content)
            self.url = selector.xpath('//a[@class="next page-numbers"]/@href').get()
            self.page_count += 1
            await asyncio.sleep(random.random())
        return article_data_list

    async def fetch_page(self) -> str:
        """
        使用 Playwright 异步获取页面 HTML 内容
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(self.url)
            # 根据需要，可以等待特定元素加载完毕或使用 wait_for_load_state
            # await page.wait_for_load_state('networkidle')
            html = await page.content()
            await browser.close()
            return html

    
