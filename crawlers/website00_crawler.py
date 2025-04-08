# crawlers/website61_crawler.py
# "name": "网站4",
# "crawler_class": __import__("crawlers.website00_crawler", fromlist=["Website00Crawler"]).Website00Crawler,
# "url": "https://www.uq.edu.au/news/",
import asyncio
from typing import Any, Dict, List
from crawlers.base_crawler import AbstractCrawler
from common import ArticleContent
from playwright.async_api import async_playwright
from parsel import Selector
from datetime import date,datetime
import random
from urllib.parse import urljoin

class Website4Crawler(AbstractCrawler):
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
            container_list = selector.xpath('//*[@id="block-system-main"]/div/div/div[1]/div')
            for container in container_list:
                parsed_content: ArticleContent = self.parse_article_content(container)
                article_data_list.append(parsed_content)
            self.url = urljoin(self.url, selector.xpath('//li[@class="pager-next last"]/a/@href').get())
            print(f"下一页连接：{self.url}")
            self.page_count += 1
            await asyncio.sleep(random.random())
        print(f"爬取完成，共爬取{len(article_data_list)}篇文章")
        print(f"爬取文章第一条：{article_data_list[0]}")
        return article_data_list
    
    def parse_article_content(self, container_selector: Selector) -> ArticleContent:
        """
        数据提取
        :param quote_item:
        :return:
        """
        article_date_str = container_selector.xpath('.//span[@class="date-display"]/text()').get()
        # 构造 ArticleContent 对象，其他字段可根据需求补充
        article = ArticleContent(
            title=container_selector.xpath('.//h3/a/text()').get(),
            author="",
            link_url=container_selector.xpath('.//h3/a/@href').get(),
            text=container_selector.xpath('.//p/text()').get(),
            nation="澳大利亚",# 无
            post_agency="昆士兰大学",# 非政府组织
            article_date = datetime.strptime(article_date_str.strip(), '%d %B %Y'),  # 使用当前日期，可根据需求调整
            # 以下默认字段，暂时不需要调整
            info_type="T0",
            domain="F0",
            subject="AG0",
        )
        return article

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

    
