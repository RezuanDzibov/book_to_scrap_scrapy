import scrapy


class BookItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()