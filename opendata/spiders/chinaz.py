# -*- coding: utf-8 -*-

from functools import partial
from urlparse import urljoin
from scrapy.utils.markup import remove_tags
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose
from scrapy.contrib.spiders import CrawlSpider, Rule
from opendata.items import ChinazItem


class ChinazSpider(CrawlSpider):

    name = 'chinaz'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://top.chinaz.com/list.aspx']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=ur'//div[@class="pagination"]/a[.="下一页"]')),
        Rule(LinkExtractor(restrict_xpaths=ur'//div[@class="webItemList"]//h3'), callback='parse_item'),
    )

    def parse_item(self, response):

        loader = ItemLoader(ChinazItem(), response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', u'//span[@id="spanwillchuanwebName"]/following-sibling::text()')
        loader.add_xpath('domain', u'//a[@id="linkUrl"]/text()')
        loader.add_xpath('homepage', u'//a[@id="linkUrl"]/@href')
        loader.add_xpath('founded', u'//span[.="建站时间:"]/following-sibling::text()')
        loader.add_xpath('company', u'//span[.="网站所属:"]/following-sibling::text()')
        loader.add_xpath('location', u'//span[.="所属地区:"]/following-sibling::a//text()')
        loader.add_xpath('founder', u'//span[.="创始人/团队:"]/following-sibling::text()')
        loader.add_xpath('categories', u'//span[.="网站类型:"]/following-sibling::a//text()')
        loader.add_xpath('rating', u'//td[b="用户评分："]/following-sibling::td/img/@src', re=r'star_(\d)')
        loader.add_xpath('keywords', u'//td[starts-with(b, "关 键 词")]/following-sibling::td/a/text()')
        loader.add_xpath('brief', u'//td[b="网站简介："]/following-sibling::td/text()')
        loader.add_xpath('alexa_rank', u'//span[.="Alexa排名:"]/following-sibling::text()')
        loader.add_xpath('baidu_weight', u'//td[.="百度权重:"]/following-sibling::td/img/@alt')
        loader.add_xpath('google_pagerank', u'//td[.="PR值:"]/following-sibling::td/img/@alt')
        loader.add_xpath('chinaz_rank', u'//td[@class="scored"]/span/text()')
        loader.add_xpath('backlink_num', u'//span[.="网站反链数: "]/following-sibling::text()')
        loader.add_xpath('keyword_num', u'//a[@id="tdgjcs"]/text()')
        loader.add_xpath('domain_birth', u'//span[.="域名年限:"]/following-sibling::text()', re=r':([0-9-]+)\)')
        loader.add_xpath('baidu_idx_num', u'//span[.="百度收录:"]/following-sibling::text()')
        loader.add_xpath('google_idx_num', u'//span[.="谷歌收录:"]/following-sibling::text()')
        loader.add_xpath('sogou_idx_num', u'//span[.="搜狗收录:"]/following-sibling::text()')
        loader.add_xpath('introduction', u'//div[h3="公司简介"]/following-sibling::div[1]', MapCompose(Compose(remove_tags, unicode.strip)))
        loader.add_xpath('snapshot', u'//figure/img/@src', MapCompose(partial(urljoin, 'http://top.chinaz.com/')))
        return loader.load_item()

