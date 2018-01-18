import scrapy
import re
from scrapy.linkextractors import LinkExtractor


class SpidySpider(scrapy.Spider):
    name = "spidy"
    allowed_domains = ["localhost"]
    start_urls = (
        'http://localhost/projectinsight.webapp/api/help',
    )
    

    def parse(self, response):
        links = ["http://localhost/projectinsight.webapp/api/help/model/apideleteresponse",
"http://localhost/projectinsight.webapp/api/help/model/apierrortype",
"http://localhost/projectinsight.webapp/api/help/model/apisaveresponse",
"http://localhost/projectinsight.webapp/api/help/model/callingconventions",
"http://localhost/projectinsight.webapp/api/help/model/charset",
"http://localhost/projectinsight.webapp/api/help/model/customattributenamedargument",
"http://localhost/projectinsight.webapp/api/help/model/customattributetypedargument",
"http://localhost/projectinsight.webapp/api/help/model/customfieldreportinputvalue",
"http://localhost/projectinsight.webapp/api/help/model/daterangefiltertype",
"http://localhost/projectinsight.webapp/api/help/model/genericparameterattributes",
"http://localhost/projectinsight.webapp/api/help/model/httpcontent",
"http://localhost/projectinsight.webapp/api/help/model/httpmethod",
"http://localhost/projectinsight.webapp/api/help/model/httppostedfilebase",
"http://localhost/projectinsight.webapp/api/help/model/httpstatuscode",
"http://localhost/projectinsight.webapp/api/help/model/idexternal",
"http://localhost/projectinsight.webapp/api/help/model/intptr",
"http://localhost/projectinsight.webapp/api/help/model/kanbanbacklogoptions",
"http://localhost/projectinsight.webapp/api/help/model/kanbansprintworkitemstatus",
"http://localhost/projectinsight.webapp/api/help/model/layoutkind",
"http://localhost/projectinsight.webapp/api/help/model/listitemvalue",
"http://localhost/projectinsight.webapp/api/help/model/membertypes",
"http://localhost/projectinsight.webapp/api/help/model/methodattributes",
"http://localhost/projectinsight.webapp/api/help/model/methodbase",
"http://localhost/projectinsight.webapp/api/help/model/methodimplattributes",
"http://localhost/projectinsight.webapp/api/help/model/methodinfo",
"http://localhost/projectinsight.webapp/api/help/model/modelpropertylist",
"http://localhost/projectinsight.webapp/api/help/model/modulehandle",
"http://localhost/projectinsight.webapp/api/help/model/nullableoft",
"http://localhost/projectinsight.webapp/api/help/model/rates",
"http://localhost/projectinsight.webapp/api/help/model/runtimemethodhandle",
"http://localhost/projectinsight.webapp/api/help/model/securityruleset",
"http://localhost/projectinsight.webapp/api/help/model/sortdirection",
"http://localhost/projectinsight.webapp/api/help/model/stream",
"http://localhost/projectinsight.webapp/api/help/model/typeattributes",
"http://localhost/projectinsight.webapp/api/help/model/typeinfo",
"http://localhost/projectinsight.webapp/api/help/model/userobjcapability",
"http://localhost/projectinsight.webapp/api/help/model/version",
"http://localhost/projectinsight.webapp/api/help/post-timer-toggle-timer"]

        #extractor = LinkExtractor(allow_domains='localhost')
        #links = extractor.extract_links(response)
        for link in links:
            #print link.url
            yield scrapy.Request(link, callback=self.parseFollow)

    def parseFollow(self, response):
        footer = "%s" % response.selector.xpath('//footer').extract_first()
        body = "%s" % response.selector.xpath('//body').extract_first()
        pageResp = "%s" % body.replace(footer, "")

        pageRespToSend = re.sub("\'", '\"', pageResp)
        pageRespToSend = re.sub(",", '\\,', pageRespToSend)
        pageRespToSend = re.sub("<sup>\\xae</sup>", '<sup>&#174;</sup>', pageRespToSend)
        #pageRespToSend = re.sub("(?!\r\n\")\r\n", '\\n', pageRespToSend) #do this replace oustide
        yield {
            "BLEHOUTPUT": "(newid(), '%s', '%s', getUtcDate())," % (response.url, pageRespToSend)
        }