import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import unicodedata


class ColossalSpider(scrapy.Spider):
    name = 'colossal_spider'
    allowed_domains = ['thisiscolossal.com']
    start_urls = [
        'https://www.thisiscolossal.com/category/Photography',
        'https://www.thisiscolossal.com/category/Craft',
        'https://www.thisiscolossal.com/category/Design',
        'https://www.thisiscolossal.com/category/Art',
        'https://www.thisiscolossal.com/category/Animation',
        'https://www.thisiscolossal.com/category/Science',
        'https://www.thisiscolossal.com/category/History',
        'https://www.thisiscolossal.com/category/Food'
    ]

    def parse(self, response):
        pagination = response.css('.pages ::text').get()
        if pagination:
            pagination_text = pagination.split(" ")
            num_pages = int(pagination_text[3])
            for page_num in range(1, num_pages + 1):
                page_url = f"{response.url}/page/{page_num}"
                yield scrapy.Request(page_url, callback=self.parse_page)

    def parse_page(self, response):
        posts = response.css('#posts').getall()
        for post in posts:
            # Extract text content and remove HTML tags
            article_text = scrapy.Selector(text=post).getall()
            for text in article_text:
                soup = BeautifulSoup(text, 'html.parser')
                p_tags = soup.find_all('p')
                p_texts = [p.text.strip() for p in p_tags if p.text.strip()]
                p_texts= convert_unicode_to_ascii(" ".join(p_texts).replace("\n"," ").replace("\t"," "))
            yield {
                'url': response.url,
                'text_content': p_texts
            }

def convert_unicode_to_ascii(text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
process = CrawlerProcess(settings={
    'FEEDS': {
        'output.json': {
            'format': 'json',
            'overwrite': True,
        },
    },
})
process.crawl(ColossalSpider)
process.start()
