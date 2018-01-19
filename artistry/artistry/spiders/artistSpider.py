# -*- coding: utf-8 -*-
import scrapy
import re
from artistry.items import ArtistryItem
import uuid
from w3lib.html import remove_tags


class ArtistspiderSpider(scrapy.Spider):
    name = 'artistSpider'
    allowed_domains = ['beatport.com']
    start_urls = ['http://beatport.com/artist/paul-van-dyk/3813/tracks']

    def parse(self, response):
        item = ArtistryItem()
        artistName = "%s" % response.css('h1').extract_first()
        item['artistName'] = artistName
        item['tracks'] = []
       
        for track in response.css('.buk-track-meta-parent'):
            trackTitle = track.css('.buk-track-title').extract_first()
            trackArtists = track.css('.buk-track-artists').extract_first()
            trackRemixers = track.css('.buk-track-remixers').extract_first()
            trackLabels = track.css('.buk-track-labels').extract_first()
            trackGenre = track.css('.buk-track-genre').extract_first()
            trackKey = track.css('.buk-track-key').extract_first()
            trackReleaseDate = track.css('.buk-track-released').extract_first()
            
            item['tracks'].append({
              u'id': remove_tags(uuid.uuid4().hex),
              u'title': remove_tags(trackTitle),
              u'artists': remove_tags(trackArtists),
              u'remixers': remove_tags(trackRemixers),
              u'labels': remove_tags(trackLabels),
              u'genre': remove_tags(trackGenre),
              u'key': remove_tags(trackKey),
              u'releaseDate': remove_tags(trackReleaseDate),
            })

        # yield item
        next_page_url = response.css(".pag-next::attr(href)").extract_first()
        if next_page_url is not None:
          return [Request(response.urljoin(next_page_url), callback=self.parse, meta={'item': item})]


        
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.innerParse)

    def innerParse(self, response):
      
