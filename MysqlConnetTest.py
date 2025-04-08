import asyncio
from async_db import MysqlConnect

async def test_db_connection():
    # 创建 MysqlConnect 的实例
    mysql_connect = MysqlConnect()

    # 异步初始化数据库连接
    await mysql_connect.async_init()

    # 获取数据库连接对象
    db = mysql_connect.get_db()

    # 执行一个简单的查询，例如获取数据库的版本信息
    sql = "SELECT VERSION();"
    version = await db.get_first(sql)

    # 打印结果
    if version:
        print(f"Database version: {version}")
        print("Database connection test successful.")
        print("数据库能正常连接")
    else:
        print("Failed to retrieve database version.")

# 运行测试函数
asyncio.run(test_db_connection())
