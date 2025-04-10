# -*- coding: utf-8 -*-
# filename: abstract_store_impl.py
# @Desc    : 存储实现工厂类
import csv
import json
import pathlib
import time
from typing import Dict,Optional
import os
from datetime import datetime

import aiofiles

from storage.abstract_store import AbstractStore
from common import ArticleContent
from async_db import AsyncMysqlDB,MysqlConnect

class StoreFactory:
    @staticmethod
    def get_store(store_type: str) -> AbstractStore:
        if store_type == "csv":
            return CsvStoreImpl()
        elif store_type == "json":
            return JsonStoreImpl()
        elif store_type == "db":
            return DbStoreImpl()
        else:
            raise ValueError(f"Unknown store type: {store_type}")


class CsvStoreImpl(AbstractStore):
    def __init__(self):
        self.csv_store_path = "data/csv"

    def make_save_file_name(self) -> str:
         # 获取当前时间
        now = datetime.now()
        # 格式化时间
        formatted_time = int(now.strftime("%Y%m%d"))
        return f"{self.csv_store_path}/article_content_{formatted_time}.csv"
    
    async def save(self,save_item: ArticleContent):
        """
        save data to csv
        :param save_item:
        :return:
        """
        pathlib.Path(self.csv_store_path).mkdir(parents=True, exist_ok=True)
        save_file_name = self.make_save_file_name()
        async with aiofiles.open(save_file_name, mode='a+', encoding="utf-8-sig", newline="") as f:
            f.fileno()
            writer = csv.writer(f)
            save_item_dict: Dict = save_item.model_dump()
            if await f.tell() == 0:
                await writer.writerow(save_item_dict.keys())
            await writer.writerow(save_item_dict.values())

class JsonStoreImpl(AbstractStore):
    def __init__(self):
        self.json_store_path = "data/json"

    def make_save_file_name(self) -> str:
        """
        make save file name
        :return:
        """
        return f"{self.json_store_path}/symbol_content_{int(time.time())}.json"

    async def save(self, save_item: ArticleContent):
        """
        save data to json
        :param save_item:
        :return:
        """
        pathlib.Path(self.json_store_path).mkdir(parents=True, exist_ok=True)
        save_file_name = self.make_save_file_name()
        save_data_list = []
        # todo 如果这里涉及并发写入，需要加锁, 可以查看MediaCrawler项目中的实现方式
        # 先判断文件是否存在，如果存在则读取文件内容放到save_data_list中，然后再将新的数据添加到save_data_list中
        if os.path.exists(save_file_name):
            async with aiofiles.open(save_file_name, 'r', encoding='utf-8') as file:
                save_data_list = json.loads(await file.read())
        save_data_list.append(save_item.model_dump())

        # 将数据写入到文件中
        async with aiofiles.open(save_file_name, 'w', encoding='utf-8') as file:
            await file.write(json.dumps(save_data_list, ensure_ascii=False))

class DbStoreImpl(AbstractStore):
    def __init__(self):
        self.db: Optional[AsyncMysqlDB] = None

    async def save(self, save_item: ArticleContent):
        """
        save data to db
        :param save_item:
        :return:
        """
        # 打印传入的 save_item
        #print(f"Saving item: {save_item}")
        self.db = (await MysqlConnect().async_init()).get_db()
        from sqls import (insert_symbol_content,
                          query_symbol_content_by_symbol,
                          update_symbol_content)

        # 查询是否存在
        exist_item = await query_symbol_content_by_symbol(self.db, save_item.link_url)
        if exist_item is not None:
            # 更新
            await update_symbol_content(self.db, save_item)
        else:
            # 插入
            await insert_symbol_content(self.db, save_item)