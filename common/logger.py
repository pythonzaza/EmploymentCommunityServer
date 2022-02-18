import logging

from configs import AppConfig

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    '%(levelname)8s %(asctime)s - %(thread)d - %(filename)s:%(lineno)d:%(funcName)s :\t%(message)s')

hd = logging.StreamHandler()

if AppConfig.config.get("debug"):
    logger.setLevel(logging.DEBUG)
    hd.setFormatter(formatter)
else:
    # hd = logging.FileHandler(f'{__name__}.log', 'a', encoding='utf-8')
    logger.setLevel(logging.INFO)
    hd.setFormatter(formatter)

logger.addHandler(hd)

__all__ = [logger]
