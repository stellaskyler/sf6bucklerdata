from scrapy.crawler import CrawlerProcess
from spiders.street_fighter_spider import StreetFighterSpider

# Create a CrawlerProcess and configure it with settings
process = CrawlerProcess(settings=StreetFighterSpider.custom_settings)
process.crawl(StreetFighterSpider)
process.start()
