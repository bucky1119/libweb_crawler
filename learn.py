# -*- coding: utf-8 -*-
# filename: learn.py
# @Desc    : 支持各种存储方式，如csv、json、db

import asyncio
import random
from typing import Any, Dict, List

import httpx
from storage.abstract_store_impl import StoreFactory
from common import ArticleContent, make_req_params_and_headers

HOST = "https://query1.finance.yahoo.com"
SYMBOL_QUERY_API_URI = "/v1/finance/screener"
PAGE_SIZE = 100  # 可选配置（25, 50, 100）


def parse_symbol_content(quote_item: Dict) -> ArticleContent:
    
    symbol_content = ArticleContent()
    symbol_content.title = quote_item["symbol"]
    symbol_content.author = quote_item["shortName"]
    symbol_content.link_url = quote_item["regularMarketPrice"]["fmt"]
    symbol_content.text = quote_item["regularMarketChange"]["fmt"]
    symbol_content.post_agency = quote_item["regularMarketChangePercent"]["fmt"]
    symbol_content.nation = quote_item["marketCap"]["fmt"]
    symbol_content.Date = quote_item["averageAnalystRating"]
    return symbol_content


async def fetch_currency_data_list(max_total_count: int) -> List[ArticleContent]:
    """
    发送请求获取数据,储存到symbol_data_list中
    :param max_total_count:
    :return:
    """
    symbol_data_list: List[ArticleContent] = []
    page_start = 0
    while page_start <= max_total_count:
        response_dict: Dict = await send_request(page_start=page_start, page_size=PAGE_SIZE)
        for quote in response_dict["finance"]["result"][0]["quotes"]:
            parsed_content: ArticleContent = parse_symbol_content(quote)
            print(parsed_content)
            symbol_data_list.append(parsed_content)
        page_start += PAGE_SIZE
        await asyncio.sleep(random.random())
    return symbol_data_list


async def send_request(page_start: int, page_size: int) -> Dict[str, Any]:
    """
    公共的发送请求的函数
    :param page_start: 分页起始位置
    :param page_size: 每一页的长度
    :return:
    """
    print(f"[send_request] page_start:{page_start}")
    req_url = HOST + SYMBOL_QUERY_API_URI
    common_params, headers, common_payload_data = make_req_params_and_headers()
    # 修改分页变动参数
    common_payload_data["offset"] = page_start
    common_payload_data["size"] = page_size

    async with httpx.AsyncClient() as client:
        response = await client.post(url=req_url, params=common_params, json=common_payload_data, headers=headers,
                                     timeout=30)
    if response.status_code != 200:
        raise Exception("发起请求时发生异常，请求发生错误，原因:", response.text)
    try:
        response_dict: Dict = response.json()
        return response_dict
    except Exception as e:
        raise e


async def get_max_total_count() -> int:
    """
    获取所有币种总数量
    :return:
    """
    print("开始获取最大的币种数量")
    try:
        response_dict: Dict = await send_request(page_start=0, page_size=PAGE_SIZE)
        total_num: int = response_dict["finance"]["result"][0]["total"]
        print(f"获取到 {total_num} 种币种")
        return total_num
    except Exception as e:
        print("错误信息：", e)
        return 0


async def run_crawler(data_save_type: str) -> None:
    """
    爬虫主流程
    :param data_save_type: 数据存储的类型，支持csv、json、db
    :return:
    """
    # step1 获取最大数据总量
    # max_total: int = await get_max_total_count()
    max_total = 100  # 测试用
    # step2 遍历每一页数据并解析存储到数据容器中
    data_list: List[ArticleContent] = await fetch_currency_data_list(max_total)
    # step3 将数据保存到指定存储介质中
    for data_item in data_list:
        await StoreFactory.get_store(data_save_type).save(data_item)


if __name__ == '__main__':
    _data_save_type = "csv"  # 可选配置（csv、json、db）
    asyncio.get_event_loop().run_until_complete(run_crawler(_data_save_type))
    # asyncio.run(run_crawler(_data_save_type))