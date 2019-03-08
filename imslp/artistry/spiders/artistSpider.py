# -*- coding: utf-8 -*-
import scrapy
import re
from imslp.items import ImslpItem
import uuid
from w3lib.html import remove_tags
import time
import datetime



class ArtistspiderSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = 'imslpSpider'
    allowed_domains = ['beatport.com']
    # start_urls = ['https://www.beatport.com/imslp/paul-van-dyk/3813/tracks']
    start_urls = ['https://www.beatport.com/imslp/placeholder/6/tracks']

    def __init__(self, category=None, *args, **kwargs):
        super(ArtistspiderSpider, self).__init__(*args, **kwargs)
        now = datetime.datetime.now()
        self.leDate = now.strftime("%Y-%m-%d %H")
        self.logFilename = "LogFile_%s.txt" % self.leDate
        self.last_time = time.time()
        self.getStartURL()
        
    def parse(self, response):
        if response.status == "404" or response.status == "500":
            yield self.moveOn(response)

        item = ImslpItem()
        self.imslpName = "%s" % response.css('h1').extract_first()
        self.imslpName = item['imslpName'] = remove_tags(self.imslpName.replace("\\", "|").replace("/", "|"))

        for track in response.xpath('//div[@class="buk-track-meta-parent"]'):
            trackTitle      = track.xpath("normalize-space(.//p[@class='buk-track-title'])").extract_first()
            trackArtists    = track.xpath("normalize-space(.//p[@class='buk-track-imslps'])").extract_first()
            trackRemixers   = track.xpath("normalize-space(.//p[@class='buk-track-remixers'])").extract_first()
            trackLabels     = track.xpath("normalize-space(.//p[@class='buk-track-labels'])").extract_first()
            trackGenre      = track.xpath("normalize-space(.//p[@class='buk-track-genre'])").extract_first()
            trackKey        = track.xpath("normalize-space(.//p[@class='buk-track-key'])").extract_first()
            trackReleaseDate = track.xpath("normalize-space(.//p[@class='buk-track-released'])").extract_first()
            
            item['track'] = {
              u'id':        remove_tags(uuid.uuid4().hex),
              u'title':     remove_tags(trackTitle.replace("\\", "|").replace("/", "|")),
              u'imslps':   remove_tags(trackArtists.replace("\\", "|").replace("/", "|")),
              u'remixers':  remove_tags(trackRemixers.replace("\\", "|").replace("/", "|")),
              u'labels':    remove_tags(trackLabels.replace("\\", "|").replace("/", "|")),
              u'genre':     remove_tags(trackGenre.replace("\\", "|").replace("/", "|")),
              u'key':       remove_tags(trackKey),
              u'releaseDate': remove_tags(trackReleaseDate),
            }
            
            yield item # every yielded item goes to the pipeline
        
        next_page_url = response.css(".pag-next::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        else:
            yield self.moveOn(response)

    def moveOn(self, resp):
        next_idx = int(resp.url.split('placeholder/')[1].split('/')[0])
        next_idx += 1
        next_url = 'http://beatport.com/imslp/placeholder/%d/tracks' % next_idx
        
        fh = open(self.logFilename, "a")
        fh.write('WORKING ON: %s' % self.imslpName.encode('utf-8') + '\n')
        fh.write("\t ||--+ %d +--||  --- %s seconds --- \n" % (next_idx - 1, time.time() - self.last_time))
        fh.close
        # self.saveStartURL(next_idx)
        self.last_time = time.time()
        
        return scrapy.Request(resp.urljoin(next_url))

    def getStartURL(self):
        fh = open("StartURL.txt", "r")
        start_idx = int(fh.readline())
        self.start_urls = ['https://www.beatport.com/imslp/placeholder/%d/tracks' % start_idx]
        fh.close

    def saveStartURL(self, newStartIdx):
        fh = open("StartURL.txt", "r")
        lines = fh.read().splitlines()
        lines[0] = newStartIdx
        fh.close
