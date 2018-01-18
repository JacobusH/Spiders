import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from loginform import fill_login_form
from lxml import html

capturedLinks = []
base_url = 'http://dev24.sandbox.projectinsight.net'

class SiteCrawlypider(scrapy.Spider):
    name = "webappsitecrawly"
    allowed_domains = ["dev24.sandbox.projectinsight.net"]
    start_urls = (
        # 'http://localhost/projectinsight.webapp/api/help',
        # 'http://dev24.sandbox.projectinsight.net/ProjectInsight.WebApp/content/dashboard/default.aspx',
        'http://dev24.sandbox.projectinsight.net/ProjectInsight.WebApp/pi-adm/user/list',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url
            , cookies={
              'ASP.NET_SessionId':'f1xlcpphbfqeesbrm1bf0s0i',
              '__zlcmid':'ingn8G0poKsFxN',
              'dev24sandboxprojectinsightnet':'t=FEFD08940DD4A0DD8714D41026A6FD627B9BB82A50ED792329716DE85F4A9D8909748D5F98AF8B0B4ECB79A87B3C7995B881666AC7B9941DC0C73D30024919A4A59A55F02B364B8EA01CA0AF102DF29735B8D66287CD1607EACC881A089B4CEAB8538AE67FEA673F655878276C8F55F4B2C5155F02B730A13C982D7C80EBD478F680E976A1363A912EC0140A63D529E2FE2A4446AF9A5EE360E5423B88897C109D71360BE74B920F59D9BE2AD3CC416421012729AF2DB3A2338FE6792B8FBD1D5B054BAED9D058A69F2BCE77F34ED44FE489E507EC04A36AFAE79AC1E7FB12B650DA69E4F4616A2DF5A4EDCACEC8D5543E6EF05EF191E09C3406AABC766C9EF7FA781338C17B84F5FC13A823D1874B714F5281516DD296DD35E76FCB11705BD18AD0C654DDE588CCB49AF5348AC680B0C6438030C1F0C731FBE1071CA25F2EAF80E5307CF3FD4BA79F113C5A331C66EB57EB73134F3092B0E82CB3E02AEC213AF001609877145A6DCADE1840465CC93A45D40F2DF0AC6503DF54002F95F801CB',
              'dev24sandboxprojectinsightnet_perm':'d=32f275f2abec4ba68cc5258b10e10f0d',
              'wp13765':'"UWAZYDs-TTXT:CDtlnDl-TZWB-UAUTDDDVICYUIDgNssDDLFl-TZWB-UAUTFJmV_U^UYTBVYAXUX"'
              }
            , callback=self.parse)
   
    def parse(self, response):
        linksToFollow = []
        extractor = LinkExtractor()
        links = extractor.extract_links(response)

        # get help link
        helpLink = "%s" % response.selector.xpath('//a[contains(@onclick, "www.projectinsight.net/manual")]').extract_first()
        helpLinkRE = re.search('(http://www.projectinsight.net.*?)\'', helpLink)
        helpLinkToShow = ''
        if(helpLinkRE is None or helpLinkRE.group(1) is None):
            helpLinkToShow = "N/A"
        else:
            helpLinkToShow = helpLinkRE.groups(1)
        
        # links to follow
        for link in links:
            newLink = link.url
            if 'dev24' not in newLink and 'projectinsight' in newLink:
                newLink = base_url + newLink
            if '?' in newLink:
                newLink = re.search('(http.*?)\?', newLink).groups(1)
            if newLink not in capturedLinks:
                linksToFollow.append(newLink)
                capturedLinks.append(newLink)

        for link in linksToFollow:
            yield { 
                "Origin, Inside, HelpLink": "%s , %s, %s" % (response.url, link, helpLinkToShow)
            }
            # yield scrapy.Request(link.url, callback=self.parse)
            yield scrapy.Request(link, callback=self.parse)