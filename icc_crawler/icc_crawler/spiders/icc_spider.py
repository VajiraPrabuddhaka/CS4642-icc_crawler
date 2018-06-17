from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.item import Item
from urllib.parse import urljoin
import re
import scrapy

class icc_spider(BaseSpider):
    name = 'icc_crawler'
    allowed_domains = ['www.icc-cricket.com']
    start_urls = ['https://www.icc-cricket.com/']

    seen = set()

    def parse(self, response):
        if response.url in self.seen:
            self.log('already seen  %s' % response.url)
        else:
            self.log('parsing  %s' % response.url)
            self.seen.add(response.url)

        hxs = HtmlXPathSelector(response)
        self.log("Response URL " + response.url)
        # if re.match(r'http://www.greenhills.co.uk/\d{4}/\d{2}/\d{2}', response.url):
        if re.match(r'https://www.icc-cricket.com/news/\d{6}', response.url):
            yield {
                    'title': hxs.select('//title/text()').extract(),
                    'url': response.url,
                }

        #     # item = BlogItem()
        #     # item['title'] = hxs.select('//title/text()').extract()
        #     # item['url'] = response.url
        #     # item['text'] = hxs.select('//section[@id="main"]//child::node()/text()').extract()
        #     self.log("yielding item " + response.url)
        #     yield {
        #         'title': hxs.select('//title/text()').extract(),
        #         'url': response.url,
        #         'text': hxs.select('//section[@id="main"]//child::node()/text()').extract(),
        #     }
            #yield item

        for url in hxs.xpath('//a/@href').extract():
            url = urljoin(response.url, url)
            if not url in self.seen and not re.search(r'.(pdf|zip|jar)$', url):
                #self.log("yielding request " + url)
                yield scrapy.Request(url, callback=self.parse)