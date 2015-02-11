# -*- coding: utf-8 -*-


import scrapy
from scrapy import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from opendata.items import *


class MywotSpider(CrawlSpider):

    name = 'mywot'
    allowed_domains = ['www.mywot.com']
    start_urls = ['https://www.mywot.com/en/scorecard']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="frame"]/ul')),
        Rule(LinkExtractor(restrict_xpaths='//span[@class="links"]'), callback='parse_item'),
    )

    def parse_item(self, response):

        sel = Selector(response)

        rank = int(sel.xpath('//p[@class="ranking-info-value"]/text()').extract()[0])
        name = domain = sel.xpath('//h2/@title').extract()[0]
        desc = sel.xpath('//p[@id="scorecard-site-description"]/text()').extract()[0]
        country = sel.xpath('//img[@id="country"]/@alt').extract()[0]
        trust, safty = sel.xpath('//div[@class="rep-explanation"]/p[1]/text()').extract()
        categories = sel.xpath('//ul[@id="category-list"]/li/a/text()').extract()
        confidences = sel.xpath('//ul[@id="category-list"]/li/a/@class').re(r'confidence-([0-9])')
        thumbnail = (sel.xpath('//img[@id="image-thumbnail"]/@src').extract() or [None])[0]

        yield MywotItem(
            mywot=response.url,
            rank=rank,
            name=name,
            domain=domain,
            country=country,
            desc=desc,
            tags=dict(zip(categories, map(int, confidences))),
            trust=trust,
            safty=safty,
            thumbnail=thumbnail,
        )

