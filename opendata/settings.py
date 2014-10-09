# -*- coding: utf-8 -*-

BOT_NAME = 'opendata'

SPIDER_MODULES = ['opendata.spiders']
NEWSPIDER_MODULE = 'opendata.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'

ITEM_PIPELINES = {
    'opendata.pipelines.OpenDataPipeline': 0
}

