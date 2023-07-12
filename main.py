from scrapy.crawler import CrawlerProcess
from spiders.street_fighter_spider import StreetFighterSpider

# Start the spider
process = CrawlerProcess(settings=StreetFighterSpider.custom_settings)
process.crawl(StreetFighterSpider)
process.start()