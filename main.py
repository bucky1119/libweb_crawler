import asyncio
from scheduler import start_scheduler
from monitoring import start_monitoring_server

async def main():
    # 启动 Prometheus 监控服务，端口可以根据需要配置
    start_monitoring_server(port=8000)
    # 启动定时任务调度器
    await start_scheduler()
    # 如果需要，等待事件循环，或添加其他初始化逻辑
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
