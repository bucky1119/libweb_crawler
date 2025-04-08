# 使用官方 Python 基础镜像（根据项目实际使用的 Python 版本选择）
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 更新系统软件包并安装必要的依赖（如 libglib2.0-0, libnss3 等）
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    wget \
    && rm -rf /var/lib/apt/lists/*
# 复制依赖配置文件到容器中
COPY requirements.txt .

# 安装项目依赖以及 Playwright 浏览器依赖
RUN pip install --no-cache-dir -r requirements.txt playwright

# 安装 Playwright 浏览器
RUN playwright install

# 安装运行浏览器所需的依赖项
RUN playwright install-deps

# 复制项目代码到容器中
COPY . .

# 暴露项目需要的端口，例如 Prometheus 监控端口 8000
EXPOSE 8000

# 容器启动时执行项目入口
CMD ["python", "main.py"]