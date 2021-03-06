# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from book_parser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']

    def __init__(self, subject):
        self.start_urls = [f'https://book24.ru/search/?q={subject}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[text() = 'Далее']/@href").extract_first()
        book_links = response.xpath("//a[@class = 'book__title-link js-item-element ddl_product_link ']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)
        yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        link = response.url
        authors = response.xpath("//a[@class = 'item-tab__chars-link js-data-link']/text()").extract()[0]
        price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        rating = response.xpath("//span[@class = 'rating__rate-value']/text()").extract_first()
        yield BookparserItem(name=name, link=link, price=price, authors=authors, rating=rating)
