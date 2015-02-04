#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opendata.items import DianpingItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.markup import remove_tags
import os.path
import urlparse


class DianpingSpider(CrawlSpider):

    name = 'dianping'
    allowed_domains = ['dianping.360.cn']
    start_urls = ['http://dianping.360.cn/']
    cache = dict()

    rules = [
        Rule(LinkExtractor(restrict_xpaths=ur'//div[@id="cat-list"]//h3'), callback='parse_list', follow=True),
        Rule(LinkExtractor(restrict_xpaths=ur'//div[contains(@class, "category-tag-inner")]'), callback='parse_list', follow=True),
        Rule(LinkExtractor(restrict_xpaths=ur'//div[@class="page"]//a[@class="next"]'), callback='parse_list', follow=True),
    ]

    def parse_list(self, response):

        sel = Selector(response)

        categories = sel.xpath('//div[@class="category-tag-tit"]/span/text()').extract()
        categories += sel.xpath('//div[contains(@class, "category-tag-inner")]/a[@class="mark"]/text()').extract()
        categories = [cate.strip('><') for cate in categories]

        for url in sel.css('#cg-right .sites-tit>a::attr(href)').extract():
            url = urlparse.urljoin(self.start_urls[0], url)
            domain = os.path.basename(url)
            yield self.cache.get(domain) or Request(url, meta={'categories': categories}, callback=self.parse_item)

    def parse_item(self, response):

        sel = Selector(response)
        name = sel.xpath('//h2[@class="site-name"]/a[1]/text()').extract()[0]
        url = sel.xpath('//h2[@class="site-name"]/a[1]/@href').extract()[0]
        rating = (sel.xpath('//div[@class="site-detail"]/span[@class="percent"]/em[contains(., "%")]/text()').extract() or ['0%'])[0].strip('%')
        cmt = sel.xpath('//div[@class="site-detail"]/span[@class="num"]/em/text()').extract()[0].strip('%')
        tags = [tag.strip('()') for tag in sel.xpath('//a[@class="mark"]/text()[1]').extract()]
        domain = os.path.basename(response.url)

        item = DianpingItem(
            name=name,
            url=url,
            rating=int(rating),
            comments={
                'all': int(cmt),
                'good': int(int(cmt)*int(rating)/100.),
                'bad': int(cmt)-int(int(cmt)*int(rating)/100.),
            },
            tags=tags,
            domain=domain,
            categories=response.meta['categories'],
            dianping=response.url,
        )

        self.cache[domain] = item

        yield item

