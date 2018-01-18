# -*- coding: utf-8 -*-
import scrapy

from kusc.items import KuscItem
from scrapy.linkextractors import LinkExtractor


class KuscspiderSpider(scrapy.Spider):
    name = "kuscspider"
    allowed_domains = ["kusc.org"]
    start_urls = (
        'http://classicalkusc.org/playlist/',
    )

    def parse(self, response):
        url = response.url + response.xpath('//td[@class="month-title"]/a/@href').extract()[0]
        self.parse_everything(response, url)
       # yield scrapy.Request(url, callback=self.parse_everything)

    def parse_everything(self, response, url):
        #print response.xpath('//td[@class="pl-music-time"]').extract()
        #print response.xpath('//td[@class="pl-music-title"]').extract()
        #print response.xpath('//table')
        
       # item = KuscItem()
       # print response.xpath('//td[@class="pl-music-time"]').extract()
       # print response.xpath('//td[@class="pl-music-title"]').extract()

       days = []
       days = response.xpath('//td[@class="calday"]/a/@href')
       for s in days:
        print s 
        
      #  for sel in response.xpath('//table'):
          #  print sel
          #  item = KuscItem()
          #  item['time'] = sel.xpath('//td[@class="pl-music-time"]'.extract())
          #  yield item

    def create_item(self, )
