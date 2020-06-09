# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst, Compose
import scrapy

# def cleaner_photo(value):
#     if value[:2] == '//':
#         return f'http:{value}'
#     return value

def to_int(num):
    return int(num)

def cleaner_price(value):
    return float(value.replace(' ', ''))

class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    #characteristics = scrapy.Field()
    pass

