from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from book_parser import settings
from book_parser.spiders.labirintru import LabirintSpider
from book_parser.spiders.book24ru import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(LabirintSpider, subject='программирование')
    process.crawl(Book24Spider, subject='программирование')
    process.start()
