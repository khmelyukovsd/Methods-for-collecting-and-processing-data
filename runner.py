from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from InstaParser import settings
from InstaParser.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    name_user = input('Enter username: ')
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider, name_user)
    process.start()