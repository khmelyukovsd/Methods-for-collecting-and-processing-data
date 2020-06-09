# -*- coding: utf-8 -*-
import scrapy
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response):
        next_page = response.xpath("//a[contains(@class,'next-paginator-button')]/@href").extract_first()
        ads_links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        yield response.follow(next_page, callback=self.parse)

    def parse_ads(self,response):
        loader = ItemLoader(item=LeroymerlinparserItem(),response=response)
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('photo', "//picture[@slot='pictures']/source[1]/@data-origin")
        loader.add_value('link', response.url)
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        #loader.add_xpath('characteristics', "//div[@class='def-list__group']/text()")
        yield loader.load_item()

