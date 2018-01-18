import scrapy
import re
from scrapy.linkextractors import LinkExtractor

capturedLinks = []

class SiteCrawlypider(scrapy.Spider):
    name = "helpdocsitecrawly"
    allowed_domains = ["localhost"]
    start_urls = (
        'http://localhost/projectinsight.webapp/api/help',
    )
    
    def parse(self, response):
        linksToFollow = []
        extractor = LinkExtractor(allow_domains='localhost')
        links = extractor.extract_links(response)

        for link in links:
            if link not in capturedLinks:
                linksToFollow.append(link)
                capturedLinks.append(link)

        for link in linksToFollow:
            yield { 
                "BLEHOUTPUT": "%s , %s" % (response.url, link.url)
            }
            yield scrapy.Request(link.url, callback=self.parse)