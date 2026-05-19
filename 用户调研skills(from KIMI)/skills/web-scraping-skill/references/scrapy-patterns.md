# Scrapy Patterns and Templates

Templates for Scrapy-based large-scale crawling with Playwright integration.

## Template 1: Basic Spider
```python
import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic_spider'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/list']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 16,
        'RETRY_TIMES': 3,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    }
    
    def parse(self, response):
        for item in response.css('.item'):
            yield {
                'title': item.css('.title::text').get(),
                'price': item.css('.price::text').get(),
                'url': item.css('a::attr(href)').get(),
            }
        
        # Pagination
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

## Template 2: Playwright-Integrated Spider
```python
import scrapy
from scrapy_playwright.page import PageMethod

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': True},
    }
    
    def start_requests(self):
        yield scrapy.Request(
            'https://spa-example.com',
            meta={'playwright': True, 'playwright_page_methods': [
                PageMethod('wait_for_selector', '.loaded-content'),
                PageMethod('evaluate', 'window.scrollTo(0, document.body.scrollHeight)'),
                PageMethod('wait_for_timeout', 2000),
            ]}
        )
    
    def parse(self, response):
        # response now contains fully rendered HTML
        for item in response.css('.dynamic-item'):
            yield {'title': item.css('h2::text').get()}
```

## Template 3: Proxy Middleware
```python
import random

class ProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(proxy_list=crawler.settings.get('PROXY_LIST', []))
    
    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = proxy
        request.headers['Proxy-Authorization'] = basic_auth_header(
            'user', 'pass'
        )
```

## Template 4: Item Pipeline (Data Processing)
```python
import json
import csv

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open(f'{spider.name}_output.json', 'w')
        self.file.write('[')
        self.first_item = True
    
    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        self.file.write(json.dumps(dict(item)))
        return item
    
    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open(f'{spider.name}_output.csv', 'w', newline='')
        self.writer = None
    
    def process_item(self, item, spider):
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
            self.writer.writeheader()
        self.writer.writerow(item)
        return item
    
    def close_spider(self, spider):
        self.file.close()
```

## Middleware Settings
```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.ProxyMiddleware': 350,
    'myproject.middlewares.RotateUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}

ITEM_PIPELINES = {
    'myproject.pipelines.JsonPipeline': 300,
    'myproject.pipelines.CsvPipeline': 400,
}

# Rate limiting
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# AutoThrottle (adaptive rate limiting)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
```
