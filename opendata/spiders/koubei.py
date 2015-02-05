#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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
    cache = dict()

    def parse(self, response):

        sel = Selector(response)
        for i in sel.css('ul.pj-rank-cate-list>li.pj-rank-cate-item'):
            cid = int(i.css('a::attr(data-id)').extract()[0])
            cname = remove_tags(i.extract()).strip()
            yield self.make_tags_ajax_request(cid, cname)

    def parse_tags_ajax(self, response):

        meta = response.meta
        cid, cname = itemgetter('cid', 'cname')(meta)
        obj = json.loads(response.body)

        if obj['status'] != 0:
            return

        for tag in obj['data']:
            ccid, ccname = itemgetter('cid', 'cname')(tag)
            ccid = str(ccid)
            yield self.make_sites_ajax_request(cid, cname, ccid, ccname, 1)

    def parse_sites_ajax(self, response):

        meta = response.meta
        cid, cname, ccid, ccname, page = itemgetter('cid', 'cname', 'ccid', 'ccname',  'page')(meta)
        obj = json.loads(response.body)

        if obj['status'] != 0:
            return

        for i in obj['data']['page']['result']:
            info = self.pick({
                'jumpurl': 'koubei',
                'sitename': 'name',
                'showurl': 'domain',
                'praise': 'rating',
            }, i)
            info['categories'] = [cname, ccname]

            item = self.cache.get(info['domain'])
            if item:
                item.update(info)
                yield item
            else:
                yield Request(info['koubei'], meta={'info':info}, callback=self.parse_page, dont_filter=True)

        if page==1:
            total = obj['data']['page']['total']
            for pg in xrange(2, total+1):
                yield self.make_sites_ajax_request(cid, cname, ccid, ccname, pg)

    def parse_page(self, response):

        info = response.meta['info']
        sel = Selector(response)
        url = sel.xpath('//p[@class="siteinfo-website"]/a/@href').extract()[0]
        tags = sel.xpath('//ul[@class="kb-tags-list"]/li/a[@class="tag-item"]/text()[1]').re(ur'(\S+)')
        cmts = map(int, sel.xpath('//div[@class="kb-site-sub-praise"]//em[@class="num"]/text()').re(ur'\(([0-9]+)\)'))

        item = KoubeiItem(
            url=url,
            tags=tags,
            comments={
                'all': sum(cmts),
                'good': cmts[0],
                'mid': cmts[1],
                'bad': cmts[2],
            },
            **self.pick(['categories', 'name', 'domain', 'rating', 'koubei'], info)
        )
        self.cache[item['domain']] = item
        yield item

    def make_tags_ajax_request(self, cid, cname):

        url = 'http://koubei.baidu.com/p/gettradetaginfoajax?tradeid=%d' % (cid,)
        return Request(url, meta={'cid': cid, 'cname': cname}, callback=self.parse_tags_ajax)

    def make_sites_ajax_request(self, cid, cname, ccid, ccname, page):

        url = 'http://koubei.baidu.com/p/gettradesitesajax?tradeid=%s&childid=%s&page=%d' % (cid, ccid, page)
        return Request(url, meta={'cid': cid, 'cname': cname, 'ccid': ccid, 'ccname': ccname, 'page': page}, callback=self.parse_sites_ajax)

    @staticmethod
    def pick(fields, obj):

        if isinstance(fields, list):
            fields = dict(zip(fields, fields))
        elif not isinstance(fields, dict):
            raise Exception()

        return {v:obj.get(k) for k,v in fields.items()}

