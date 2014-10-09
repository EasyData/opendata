#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from jsonpath import jsonpath
from operator import itemgetter
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.utils.markup import remove_tags
from opendata.items import KoubeiItem


class KoubeiSpider(Spider):

    name = "koubei"
    allowed_domains = ["koubei.baidu.com"]
    start_urls = ['http://koubei.baidu.com/rank']

    def parse(self, response):

        sel = Selector(response)
        for i in sel.css('ul.pj-rank-cate-list>li.pj-rank-cate-item'):
            cid = int(i.css('a::attr(data-id)').extract()[0])
            cname = remove_tags(i.extract()).strip()
            yield self.make_ajax_request(cid, cname, 1)

    def parse_ajax(self, response):

        meta = response.meta
        cid, cname, page = itemgetter('cid', 'cname', 'page')(meta)
        obj = json.loads(response.body)

        if jsonpath(obj, '$.status')[0]!=0:
            return

        for i in jsonpath(obj, '$.data.page.result.*'):
            info = self.pick({
                'jumpurl':'url',
                'sitename':'name',
                'showurl':'domain',
                'praise':'rating',
                'comtcount':'comment_num'
            }, i)
            info['category'] = cname
            yield Request(info['url'], meta={'info':info}, callback=self.parse_page)

        if page==1:
            total = jsonpath(obj, '$.data.page.total')[0]
            for pg in xrange(2, total+1):
                yield self.make_ajax_request(cid, cname, pg)

    def parse_page(self, response):

        info = response.meta['info']
        sel = Selector(response)
        homepage = sel.xpath('//div[@class="pj-site-domain"]/a/@href').extract()[0]
        tags = sel.xpath('//a[contains(@class,"tag-item-link")]/text()[1]').re(ur'(\S+)[(]')
        yield KoubeiItem(
            homepage=homepage,
            tags=tags,
            **self.pick(['url', 'category', 'name', 'domain', 'rating', 'comment_num'], info)
        )

    def make_ajax_request(self, cid, cname, page):

        url = 'http://koubei.baidu.com/p/gettradesitesajax?tradeid=%s&childid=0&page=%d'%(cid, page)
        return Request(url, meta={'cid':cid, 'cname':cname, 'page':1}, callback=self.parse_ajax)

    @staticmethod
    def pick(fields, obj):

        if isinstance(fields, list):
            fields = dict(zip(fields, fields))
        elif not isinstance(fields, dict):
            raise Exception()

        return {v:obj.get(k) for k,v in fields.items()}

