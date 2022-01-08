import scrapy
from scrapy import Selector


class LibrarySpider(scrapy.Spider):
    name = 'books_to_scrap'
    start_urls = ['http://books.toscrape.com/index.html']
    
    def parse(self, response, **kwargs):
        books = response.css('article.product_pod').getall()
        for book in books:
            book = Selector(text=book)
            book_link = book.css('h3 a::attr(href)')[0]
            yield response.follow(book_link, self.parse_book)
        for next_page in response.css('li.next a::attr(href)'):
            yield response.follow(next_page, self.parse)
            
    def parse_book(self, response, **kwargs):
        book_name = response.css('div.product_main h1::text').get().strip()
        book_price = response.css('p.price_color::text').get().strip()
        book_image = response.css('div.carousel-inner img::attr(src)').get()
        book_description = response.xpath('/html/body/div/div/div[2]/div[2]/article/p/text()').get()
        book_upc = response.xpath('/html/body/div/div/div[2]/div[2]/article/table/tbody/tr[1]/td')