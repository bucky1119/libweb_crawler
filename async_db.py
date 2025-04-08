# -*- coding: utf-8 -*-
# filename: async_db.py
# @Desc    : 异步数据库

import os
from typing import Any, Dict, List, Optional, Union

import aiomysql


class AsyncMysqlDB:
    def __init__(self, pool: aiomysql.Pool) -> None:
        self.__pool = pool

    async def query(self, sql: str, *args: Union[str, int]) -> List[Dict[str, Any]]:
        """
        从给定的 SQL 中查询记录，返回的是一个列表
        :param sql: 查询的sql
        :param args: sql中传递动态参数列表
        :return:
        """
        async with self.__pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                data = await cur.fetchall()
                return data or []

    async def get_first(self, sql: str, *args: Union[str, int]) -> Union[Dict[str, Any], None]:
        """
        从给定的 SQL 中查询记录，返回的是符合条件的第一个结果
        :param sql: 查询的sql
        :param args:sql中传递动态参数列表
        :return:
        """
        async with self.__pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                data = await cur.fetchone()
                return data

    async def item_to_table(self, table_name: str, item: Dict[str, Any]) -> int:
        """
        表中插入数据
        :param table_name: 表名
        :param item: 一条记录的字典信息
        :return: 插入记录的ID
        """
        # 获取字典的键列表，作为插入表的字段名
        fields = list(item.keys())
        # 获取字典的值列表，作为插入表的字段值
        values = list(item.values())
        # 将字段名用反引号包裹，防止字段名与SQL关键字冲突
        fields = [f'`{field}`' for field in fields]
        # 将字段名列表转换为逗号分隔的字符串
        fieldstr = ','.join(fields)
        # 生成与字段值数量相同的占位符字符串，用于SQL语句
        valstr = ','.join(['%s'] * len(item))
        # 构造插入数据的SQL语句
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (table_name, fieldstr, valstr)
        # 从连接池中获取一个数据库连接
        async with self.__pool.acquire() as conn:
            # 使用DictCursor游标类型，以便获取结果为字典形式
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 执行插入数据的SQL语句，并传入字段值列表
                await cur.execute(sql, values)
                # 获取插入记录的ID
                lastrowid = cur.lastrowid
                # 返回插入记录的ID
                return lastrowid

    async def update_table(self, table_name: str, updates: Dict[str, Any], field_where: str,
                           value_where: Union[str, int, float]) -> int:
        """
        更新指定表的记录
        :param table_name: 表名
        :param updates: 需要更新的字段和值的 key - value 映射
        :param field_where: update 语句 where 条件中的字段名
        :param value_where: update 语句 where 条件中的字段值
        :return:
        """
        upsets = []
        values = []
        for k, v in updates.items():
            s = '`%s`=%%s' % k
            upsets.append(s)
            values.append(v)
        upsets = ','.join(upsets)
        sql = 'UPDATE %s SET %s WHERE %s="%s"' % (
            table_name,
            upsets,
            field_where, value_where,
        )
        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                rows = await cur.execute(sql, values)
                return rows

    async def execute(self, sql: str, *args: Union[str, int]) -> int:
        """
        需要更新、写入等操作的 excute 执行语句
        :param sql:
        :param args:
        :return:
        """
        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                rows = await cur.execute(sql, args)
                return rows
class MysqlConnect:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # 检查当前类是否已经创建了实例
        if cls._instance is None:
            # 如果没有实例，则调用父类的__new__方法创建一个新的实例
            cls._instance = super(MysqlConnect, cls).__new__(cls, *args, **kwargs)
        # 返回当前类的唯一实例
        return cls._instance

    def __init__(self):
        # 初始化方法，用于创建类的实例时调用
        self.db: Optional[AsyncMysqlDB] = None

    async def async_init(self):
        # 检查对象是否具有'db'属性，或者'db'属性是否为None
        if not hasattr(self, 'db') or self.db is None:
            # 使用aiomysql库创建一个数据库连接池
            # 将self.mysql_conn_config中的配置参数解包传递给create_pool函数
            # 设置autocommit为True，表示自动提交事务
            pool = await aiomysql.create_pool(
                **self.mysql_conn_config,
                autocommit=True,
            )
            # 创建一个AsyncMysqlDB实例，将连接池传递给它
            self.db: AsyncMysqlDB = AsyncMysqlDB(pool)
        # 返回当前对象实例
        return self

    #@property装饰器用于将一个方法转换为只读属性。
    #这意味着你可以像访问属性一样访问这个方法，而不需要调用它。
    @property
    def mysql_conn_config(self) -> Dict[str, str]:
        return {
            # "host": os.getenv("MYSQL_HOST", "localhost"),
            # "port": int(os.getenv("MYSQL_PORT", 3306)),
            # "user": os.getenv("MYSQL_USER", "root"),
            # "password": os.getenv("MYSQL_PASSWORD", "123456"),
            # "db": os.getenv("MYSQL_DB", "crawler_data"),
            "host": os.getenv("MYSQL_HOST", "101.200.87.86"),
            "port": int(os.getenv("MYSQL_PORT", 3306)),
            "user": os.getenv("MYSQL_USER", "libweb"),
            "password": os.getenv("MYSQL_PASSWORD", "bucky123@123!"), # 将密码转换为字节串
            "db": os.getenv("MYSQL_DB", "my_database"),
        }
    
    # 定义一个名为 get_db 的方法，该方法属于某个类（self 表示类的实例），返回类型为 AsyncMysqlDB
    def get_db(self) -> AsyncMysqlDB:  
        return self.db  # 返回当前实例（self）的 db 属性，该属性应该是 AsyncMysqlDB 类型的数据库连接对象