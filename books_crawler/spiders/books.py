from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request



class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)
            
            #process next page
        next_page_url =response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url =response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)
            
        
    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        img_url = response.xpath('//img/@src').extract_first()
        img_url = img_url.replace('../..', 'http://books.toscrape.com/')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath(
            '//*[@id="product_description"]/following-sibling::p/text()').extract_first()
        
        yield {
            'title':title,
            'price':price,
            'img_url':img_url,
            'rating':rating,
            'description':description}
        
        
    
    
   

# Trial with selenium
# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
    
#     def start_requests(self):
#         self.driver = webdriver.Firefox()
#         self.driver.get('http://books.toscrape.com/index.html')
        
#         sel = Selector(text=self.driver.page_source)
    
#         books = sel.xpath('//h3/a/@href').extract()
#         for book in books:
#             url = 'http://books.toscrape.com/'+book
#             yield Request(url, callback=self.parse_book)
            
#     def parse_book(self, response):
#         pass


# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

# class BooksSpider(CrawlSpider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     start_urls = ['http://books.toscrape.com/']
    
#     rules = (Rule(LinkExtractor( deny_domains='google.com'), callback='parse_page', follow=False),)

#     def parse_page(self, response):
#         yield {'URL':response.url}
