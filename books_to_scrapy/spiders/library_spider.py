import scrapy
from scrapy import Selector


class LibrarySpider(scrapy.Spider):
    name = 'books_to_scrap'
    start_urls = ['http://books.toscrape.com/index.html']
    
    def parse(self, response, **kwargs):
        books = response.css('article.product_pod').getall()
        for book in books:
            book = Selector(text=book)
            book_name = book.css('h3')
            book_name = book_name.css('a::text').get()
            print(book_name)