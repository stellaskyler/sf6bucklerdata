import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

class RandomUserAgentMiddleware(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class RetryChangeProxyMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)

    def process_response(self, request, response, spider):
        if response.status in [403, 401, 429, 405, 500]:
            spider.consecutive_errors += 1  # Increment the error count
            spider.adjust_delay()  # Adjust the delay based on the error count
            return self._retry(request, f'{response.status} error', spider) or response
        spider.consecutive_errors = 0  # Reset the error count if the page is successfully parsed
        return response
