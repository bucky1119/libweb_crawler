# crawlers/website3_crawler.py
# "name": "网站3",
# "crawler_class": __import__("crawlers.website3_crawler", fromlist=["Website3Crawler"]).Website3Crawler,
# "url": "https://www.agriculture.gov.au/about/news/all?f%5B0%5D=topic%3A310",
import asyncio
from typing import Any, Dict, List
from crawlers.base_crawler import AbstractCrawler
from common import ArticleContent
from playwright.async_api import async_playwright
from parsel import Selector
from datetime import date
import random
from urllib.parse import urljoin

class Website3Crawler(AbstractCrawler):
    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get("url")
        # 其他配置参数，比如请求头、超时设置等可以在此处初始化
        # 是否翻页运行标志
        self.running_state = True
        # 翻页计数器
        self.page_count = 1
        # 限制爬取页数
        self.PAGE_SIZE = 1

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
            #print(html)
            selector = Selector(text=html)
            container_list = selector.xpath('//*[@id="block-system-main-block"]//div[@class="view-content"]/div')
            for container in container_list:
                parsed_content: ArticleContent = self.parse_article_content(container)
                article_data_list.append(parsed_content)
            self.url = urljoin(self.url, selector.xpath('//a[@title="Go to next page"]/@href').get())
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
        # 构造 ArticleContent 对象，其他字段可根据需求补充
        article = ArticleContent(
            title=container_selector.xpath('.//h3/a/text()').get(),
            author="",
            link_url=urljoin(self.url, container_selector.xpath('.//h3/a/@href').get()),
            text = container_selector.xpath('.//div[@class="views-field views-field-body"]/span/text()').get(),
            nation="澳大利亚",# 
            post_agency="悉尼大学",# 非政府组织
            article_date = container_selector.xpath('.//div[@class="views-field views-field-created"]/span/time/@datetime').get().split('T')[0], 
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

    
