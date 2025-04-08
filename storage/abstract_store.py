# -*- coding: utf-8 -*-
# filename: abstract_store.py
# @Desc    : 抽象存储类

from abc import ABC, abstractmethod
from common import ArticleContent

class AbstractStore(ABC):
    @abstractmethod
    async def save(self,article:ArticleContent):
        """
        存储数据
        :param save_item:
        :return:
        """
        raise NotImplementedError