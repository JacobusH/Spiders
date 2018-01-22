# -*- coding: utf-8 -*-
import scrapy
import re
from artistry.items import ArtistryItem
import uuid
from w3lib.html import remove_tags



class ArtistspiderSpider(scrapy.Spider):
    name = 'artistSpider'
    allowed_domains = ['beatport.com']
    # start_urls = ['https://www.beatport.com/artist/paul-van-dyk/3813/tracks']
    start_urls = ['https://www.beatport.com/artist/placeholder/1/tracks']

    def parse(self, response):
        item = ArtistryItem()
        artistName = "%s" % response.css('h1').extract_first()
        item['artistName'] = remove_tags(artistName)


        for track in response.xpath('//div[@class="buk-track-meta-parent"]'):
            trackTitle      = track.xpath("normalize-space(.//p[@class='buk-track-title'])").extract_first()
            trackArtists    = track.xpath("normalize-space(.//p[@class='buk-track-artists'])").extract_first()
            trackRemixers   = track.xpath("normalize-space(.//p[@class='buk-track-remixers'])").extract_first()
            trackLabels     = track.xpath("normalize-space(.//p[@class='buk-track-labels'])").extract_first()
            trackGenre      = track.xpath("normalize-space(.//p[@class='buk-track-genre'])").extract_first()
            trackKey        = track.xpath("normalize-space(.//p[@class='buk-track-key'])").extract_first()
            trackReleaseDate = track.xpath("normalize-space(.//p[@class='buk-track-releaseDate'])").extract_first()
            
            item['track'] = {
              u'id':        remove_tags(uuid.uuid4().hex),
              u'title':     remove_tags(trackTitle),
              u'artists':   remove_tags(trackArtists),
              u'remixers':  remove_tags(trackRemixers),
              u'labels':    remove_tags(trackLabels),
              u'genre':     remove_tags(trackGenre),
              u'key':       remove_tags(trackKey),
              u'releaseDate': remove_tags(trackReleaseDate),
            }
            
            yield item # every yielded item goes to the pipeline
        
        next_page_url = response.css(".pag-next::attr(href)").extract_first()
        if next_page_url is not None:
            print "NEXT PAGE: %s" % next_page_url
            yield scrapy.Request(response.urljoin(next_page_url))
        else:
            next_idx = int(response.url.split('placeholder/')[1].split('/')[0])
            next_idx += 1
            next_url = 'http://beatport.com/artist/placeholder/%s/tracks' % str(next_idx)
            self.logger.info('FINISHED: %s') % str(item['artistName'])
            self.logger.info('WORKING ON: %s') % next_url
            yield scrapy.Request(response.urljoin(next_page_url))

    
