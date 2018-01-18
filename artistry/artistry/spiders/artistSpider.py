# -*- coding: utf-8 -*-
import scrapy
import re
from artistry.items import ArtistryItem


class ArtistspiderSpider(scrapy.Spider):
    name = 'artistSpider'
    allowed_domains = ['beatport.com']
    start_urls = ['http://beatport.com/artist/paul-van-dyk/3813']

    def parse(self, response):
        # footer = "%s" % response.selector.xpath('//footer').extract_first()
        # body = "%s" % response.selector.xpath('//body').extract_first() #change to use <article id="body" class="help-page">
        artistName = "%s" % response.selector.xpath('//h1').extract_first()
        
        item = ArtistryItem()
        item['artistName'] = artistName
        yield item
