# monitoring.py
from prometheus_client import start_http_server, Counter, Gauge, Summary

# 统计成功和失败的任务数
TASK_SUCCESS_COUNT = Counter('task_success_total', '总成功任务数')
TASK_FAILURE_COUNT = Counter('task_failure_total', '总失败任务数')

# 当前正在执行的任务数量
CURRENT_TASKS = Gauge('current_running_tasks', '当前正在运行的任务数')

# 记录每个任务的执行时间
TASK_EXECUTION_TIME = Summary('task_execution_seconds', '任务执行时间')

def start_monitoring_server(port=8000):
    """
    启动 Prometheus 监控服务
    """
    start_http_server(port)
