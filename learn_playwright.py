import asyncio
from playwright.async_api import async_playwright
from common import ArticleContent
from typing import Any, Dict, List
from datetime import date
from parsel import Selector

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # url = 'https://www.baidu.com'
        url = 'https://foodtank.com/news/category/food-tank/'
        await page.goto(url)
        symbol_data_list: List[ArticleContent] = []
        running_state = True
        while running_state:
              html = await fetch_page(url)
              parsed_content: List[ArticleContent] = parse_ariticle_content(html)
              symbol_data_list.extend(parsed_content)
        print(await page.title())
        print(html)
        # await page.screenshot(path='example.png')
        await browser.close()

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

def parse_ariticle_content(self, html: str) -> ArticleContent:
        """
        解析页面 HTML 内容，提取标题、文本等信息构造 ArticleContent 对象
        """
        selector = Selector(text=html)
        # 示例：提取页面标题
        title = selector.xpath("//title/text()").get() or "Untitled"
        # 示例：提取页面主体文本（可以根据实际页面结构调整）
        text_list = selector.xpath("//body//text()").getall()
        text = "\n".join([t.strip() for t in text_list if t.strip()])

        # 构造 ArticleContent 对象，其他字段可根据需求补充
        article = ArticleContent(
            title=title.strip(),
            author="",
            link_url=self.url,
            text=text,
            nation="",
            post_agency="",
            article_date=str(date.today()),  # 使用当前日期，可根据需求调整
            # 以下默认字段，暂时不需要调整
            info_type="T0",
            domain="F0",
            subject="AG0",
        )
        return article

asyncio.run(main())
