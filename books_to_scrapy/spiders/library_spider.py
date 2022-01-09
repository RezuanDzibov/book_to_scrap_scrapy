import scrapy
from scrapy import Selector
from scrapy.http import TextResponse

from books_to_scrapy.items import BookItem


BASE_URL = 'http://books.toscrape.com/index.html'


def get_book_links(response: TextResponse) -> list:
    book_link_list = list()
    books = response.css('article.product_pod').getall()
    for book in books:
        book = Selector(text=book)
        book_link = book.css('h3 a::attr(href)').get()
        book_link_list.append(book_link)
    return book_link_list

            
def parse_book(response: TextResponse, **kwargs):
    item = BookItem()
    item['name'] = response.css('div.product_main h1::text').get().strip() # type: ignore
    item['price'] = response.css('p.price_color::text').get().strip() # type: ignore
    item['image'] = response.urljoin(response.css('div.carousel-inner img::attr(src)').get())
    item['description'] = response.xpath('/html/body/div/div/div[2]/div[2]/article/p/text()').get()
    book_table_content = response.css('table td::text').getall()
    item['upc'] = book_table_content[0]
    item['tax'] = book_table_content[4]
    item['availability'] = book_table_content[5]
    item['star_rating'] = response.css('p.star-rating').xpath("@class").extract()[0].split()[-1]
    yield item


class LibrarySpider(scrapy.Spider):
    name = 'books_to_scrape'
    start_urls = [BASE_URL]
    
    def parse(self, response: TextResponse, **kwargs):
        book_links = get_book_links(response=response)
        for book_link in book_links:
            yield response.follow(book_link, parse_book)
        for next_page in response.css('li.next a::attr(href)'):
            yield response.follow(next_page, self.parse)
        

class LibraryCategorySpider(scrapy.Spider):
    name = 'books_to_scrape_category'
    start_urls = [BASE_URL]
    
    def __init__(self, category: str, *args, **kwargs):
        """[summary]
        Args:
            category (str): If you need to provide a category name with spaces.
            You must use underscore instated of spaces.
        """
        super().__init__(*args, **kwargs)
        self.category: str = category.replace('_', ' ')
        
    def parse(self, response: TextResponse, **kwargs):
        category_links = response.xpath(f"//*[contains(text(),'{self.category}')]")
        for category_link in category_links:
            if category_link.xpath('text()').get().strip() == self.category:
                yield response.follow(
                    response.urljoin(category_link.xpath('@href').get()), 
                    callback=self.parse_category_books
                )

    def parse_category_books(self, response: TextResponse, **kwargs):
        book_links = get_book_links(response=response)
        for book_link in book_links:
            yield response.follow(book_link, parse_book)
        for next_page in response.css('li.next a::attr(href)'):
            yield response.follow(next_page, self.parse)