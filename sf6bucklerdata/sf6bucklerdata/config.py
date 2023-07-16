import logging

# Configuration for logging module
LOGGING_CONFIG = {
    'format': '%(asctime)s [%(levelname)s] %(message)s',
    'level': logging.INFO
}

# Common settings for Scrapy spiders
COMMON_SPIDER_SETTINGS = {
    'RETRY_TIMES': 5,
    'RETRY_HTTP_CODES': [403, 401, 429, 405],
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        '__main__.RetryChangeProxyMiddleware': 540,
        '__main__.RandomUserAgentMiddleware': 400,
        'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 300,
    },
    'HTTPCACHE_ENABLED': True,
    'HTTPCACHE_EXPIRATION_SECS': 0,  # Set to 0 to never expire
    'HTTPCACHE_DIR': 'httpcache',
    'HTTPCACHE_IGNORE_HTTP_CODES': [],  # HTTP codes not to cache
    'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
    'DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 32,  # Set the maximum number of concurrent requests
    'AUTOTHROTTLE_ENABLED': True,  # Enable AutoThrottle to automatically adjust concurrency and delay
    'AUTOTHROTTLE_START_DELAY': 0.5,  # The initial download delay
    'AUTOTHROTTLE_MAX_DELAY': 60,  # The maximum download delay to be set in case of high latencies
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # The average number of requests Scrapy should be sending in parallel to each remote server
    'USER_AGENTS': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.54',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.90',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.1.2369.21',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0.2',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0.3',
    ],
    'AUTOTHROTTLE_DEBUG': False,  # Enable (or disable) the AutoThrottle extension debug mode
}
