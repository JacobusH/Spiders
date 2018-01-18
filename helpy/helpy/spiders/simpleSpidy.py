# -*- coding: utf-8 -*-
import scrapy
import re
from helpy.items import SimpleSpidyItem


class SimplespidySpider(scrapy.Spider):
    name = 'simpleSpidy'
    allowed_domains = ["localhost"]

    def __init__(self, currentUrl='', *args, **kwargs):
        super(SimplespidySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['%s' % currentUrl]

    def parse(self, response):
        footer = "%s" % response.selector.xpath('//footer').extract_first()
        body = "%s" % response.selector.xpath('//body').extract_first() #change to use <article id="body" class="help-page">
        pageResp = "%s" % body.replace(footer, "")

        pageRespToSend = re.sub("\'", '\"', pageResp)
        pageRespToSend = re.sub(",", '\\,', pageRespToSend)
        pageRespToSend = re.sub("<sup>\\xae</sup>", '<sup>&#174;</sup>', pageRespToSend)
        # yield {
        #     "BLEHOUTPUT": "(newid(), '%s', '%s', getUtcDate())," % (response.url, pageRespToSend)
        # }
        
        item = SimpleSpidyItem()
        item['sqlStmt'] = "\n\ninsert into helpdoc values(newid(), '%s', '%s', getUtcDate())" % (response.url, pageRespToSend)
        yield item
