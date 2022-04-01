import logging
from datetime import datetime

from configs import AppConfig

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    '%(levelname)8s %(asctime)s - %(thread)d - %(filename)s:%(lineno)d:%(funcName)s :\t%(message)s')

hd = logging.StreamHandler()

if AppConfig.get("debug"):
    logger.setLevel(logging.DEBUG)
    hd.setFormatter(formatter)
else:
    hd = logging.FileHandler(f"./log/{datetime.now().strftime('%Y-%m-%d')}.log", 'a', encoding='utf-8')
    logger.setLevel(logging.INFO)
    hd.setFormatter(formatter)

logger.addHandler(hd)

__all__ = [logger]
