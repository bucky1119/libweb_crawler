# log.py
import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加 handler
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # 文件处理器：日志文件最多 10MB，备份 5 个文件
        os.makedirs("logs", exist_ok=True)
        fh = RotatingFileHandler(os.path.join("logs", f"{name}.log"), maxBytes=10*1024*1024, backupCount=5,encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
