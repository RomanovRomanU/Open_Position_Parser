# -*- coding: utf-8 -*-
from scrapy import Item, Field


class OpenPostion(Item):
    name = Field()
    href = Field()
    company_name = Field()
    description = Field()
