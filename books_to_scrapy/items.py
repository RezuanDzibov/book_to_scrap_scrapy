import scrapy


class BooksItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    availability = scrapy.Field()
    tax = scrapy.Field()