# -*- coding: utf-8 -*-


import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from opendata.items import *


class AlexaSpider(CrawlSpider):

    name = 'alexa'
    allowed_domains = ['alexa.com']
    start_urls = ['http://www.alexa.com/topsites/countries']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"categories")]'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="alexa-pagination"]/a[@class="next"]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        raise NotImplementedError()

