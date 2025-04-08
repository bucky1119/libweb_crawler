# -*- coding: utf-8 -*-
# filename: sqls.py

from async_db import AsyncMysqlDB
from common import ArticleContent
from typing import Optional

async def insert_symbol_content(db: AsyncMysqlDB, symbol_content: ArticleContent) -> int:
    """
    插入数据
    :param db: 异步MySQL数据库连接对象
    :param symbol_content: 要插入的文章内容对象
    :return: 插入操作的结果，通常是一个整数表示影响的行数
    """
    # 将文章内容对象转换为字典形式，以便于插入数据库
    item = symbol_content.model_dump()
    # 调用数据库连接对象的item_to_table方法，将数据插入到指定的表中
    # "web_data_table" 是目标表的名称
    # item 是要插入的数据
    return await db.item_to_table("web_data_table", item)


async def update_symbol_content(db: AsyncMysqlDB, symbol_content: ArticleContent) -> int:
    """
    更新数据
    :param db:
    :param symbol_content:
    :return:
    """
    item = symbol_content.model_dump()
    return await db.update_table("web_data_table", item, "link_url", symbol_content.link_url)


async def query_symbol_content_by_symbol(db: AsyncMysqlDB, symbol: str) -> Optional[ArticleContent]:
    """
    查询数据
    :param db:
    :param symbol:
    :return:
    """
    sql = f"select * from web_data_table where link_url = %s"
    rows = await db.query(sql, (symbol,))
    if len(rows) > 0:
        return ArticleContent(**rows[0])
    return None  # 当没有找到匹配的记录时返回 None