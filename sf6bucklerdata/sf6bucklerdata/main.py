from scrapy.crawler import CrawlerProcess
from spiders.street_fighter_spider import StreetFighterSpider

import logging
from config import LOGGING_CONFIG

logging.basicConfig(**LOGGING_CONFIG)

# Create a CrawlerProcess and configure it with settings
process = CrawlerProcess(settings=StreetFighterSpider.custom_settings)
process.crawl(StreetFighterSpider)
process.start()
