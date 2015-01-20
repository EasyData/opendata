# -*- coding: utf-8 -*-

from scrapy import Item, Field


class OpenDataItem(Item):

    time = Field()


class AlexaItem(OpenDataItem):

    name    = Field()
    domain  = Field()
    country = Field()
    desc    = Field()


class KoubeiItem(OpenDataItem):

    url      = Field()
    name     = Field()
    domain   = Field()
    rating   = Field()
    category = Field()
    tags     = Field()
    comments = Field()
    koubei   = Field()


class ChinazItem(OpenDataItem):

    url             = Field()
    name            = Field()
    domain          = Field()
    homepage        = Field()
    founded         = Field()
    company         = Field()
    location        = Field()
    founder         = Field()
    categories      = Field()
    rating          = Field()
    keywords        = Field()
    brief           = Field()
    alexa_rank      = Field()
    baidu_weight    = Field()
    google_pagerank = Field()
    chinaz_rank     = Field()
    backlink_num    = Field()
    keyword_num     = Field()
    domain_birth    = Field()
    baidu_idx_num   = Field()
    google_idx_num  = Field()
    sogou_idx_num   = Field()
    introduction    = Field()
    snapshot        = Field()

