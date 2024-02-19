import scrapy
from scrapy.crawler import CrawlerProcess
import time
import re
from twisted.internet import asyncioreactor
import asyncio
import unicodedata


asyncioreactor.install(asyncio.get_event_loop())

class MySpider(scrapy.Spider):
    name = "my_spider"

    def start_requests(self):

        with open('../../../bizBashLinks.txt', 'r') as file:
            links = file.readlines()
        
        for link in links:
            yield scrapy.Request(url=link.strip(), callback=self.parse)

    def parse(self, response):
        text_content = response.css('.page-contents__content-body p ::text').getall()

        text_content = ' '.join(text_content).strip().replace("  ","")

        text_content = self.filter_commented_content(text_content)
        text_content = self.convert_unicode_to_ascii(text_content)


        yield {
            'url': response.url,
            'text_content': text_content
        }

    def filter_commented_content(self, text):
        cleaned_text = re.sub(r'/\*.*?\*/', '', text)
        return cleaned_text
    def convert_unicode_to_ascii(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

process = CrawlerProcess(settings={
    'FEEDS': {
        'output.json': {
            'format': 'json',
            'overwrite': True,
        },
    },
})
process.crawl(MySpider)
process.start()