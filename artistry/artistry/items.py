# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtistryItem(scrapy.Item):
    # define the fields for your item here like:
    artistName = scrapy.Field()
    track = scrapy.Field()
    pass
