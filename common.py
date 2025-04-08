# -*- coding: utf-8 -*-
# filename: common.py
# @Desc    : 公共代码，包含模型类定义、请求头参数构造
from pydantic import BaseModel, Field
from datetime import date 
from typing import Optional
class ArticleContent(BaseModel):
    title:str = Field(default=...,title="标题")
    author:str = Field(default="",title="作者")
    info_type:str = Field(default="T0",title="信息类型")
    post_agency:str = Field(default="",title="发布机构")
    nation:str = Field(default="",title="国家")
    article_date: Optional[date] = Field(default=None, title="日期")
    link_url:str = Field(default=...,title="链接")
    domain:str = Field(default="F0",title="领域")
    subject:str = Field(default="AG0",title="学科")
    text: Optional[str] = Field(default=None,title="文本")   