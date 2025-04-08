import asyncio
from playwright.async_api import async_playwright
from common import ArticleContent
from typing import Any, Dict, List
from datetime import date,datetime
from parsel import Selector
import random
from urllib.parse import urljoin

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # url = 'https://www.baidu.com'
        url = 'https://www.uq.edu.au/news/'
        print(url)
        # await page.goto(url)
        running_state = True
        article_data_list: List[ArticleContent] = []
        page_count =1
        PAGE_SIZE = 5


        
        while running_state and page_count <= PAGE_SIZE:
            html = await fetch_page(url)
            selector = Selector(text=html)
            # container_list = selector.xpath('//*[@id="block-system-main"]/div/div/div[1]/div')
            # for container in container_list:
            #     parsed_content: ArticleContent = parse_article_content(container)
            #     article_data_list.append(parsed_content)
            url = urljoin(url, selector.xpath('//li[@class="pager-next last"]/a/@href').get())
            print(url)
            page_count += 1
            await asyncio.sleep(random.random())
            print(await page.title())
        print(len(article_data_list))
        print(page_count)


async def fetch_page(url: str) -> str:
        """
        使用 Playwright 异步获取页面 HTML 内容
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            # 根据需要，可以等待特定元素加载完毕或使用 wait_for_load_state
            # await page.wait_for_load_state('networkidle')
            html = await page.content()
            await browser.close()
            return html

def parse_article_content(container_selector: Selector) -> ArticleContent:
    article_date_str = container_selector.xpath('//span[@class="date-display"]/text()').get()
        # 构造 ArticleContent 对象，其他字段可根据需求补充
    print(article_date_str)
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

asyncio.run(main())
