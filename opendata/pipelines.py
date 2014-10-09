# -*- coding: utf-8 -*-

import time


class OpenDataPipeline(object):

    def process_item(self, item, spider):

        item['time'] = time.time()
        return item

