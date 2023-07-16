logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


class StreetFighterSpider(scrapy.Spider):
    name = "street_fighter_spider"
    custom_settings = {
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

    players_per_rank = {'m': 13978, 'd': 56252, 'p': 266185, 'g': 229197, 's': 282945, 'b': 205462, 'i': 209900}
    pages_per_rank = {}
    current_page = 0

    for rank in players_per_rank:
        start_page = current_page + 1
        end_page = current_page + players_per_rank[rank] // 20
        pages_per_rank[rank] = (start_page, end_page)
        current_page = end_page

    sampled_pages_per_rank = {rank: set() for rank in players_per_rank}
    valid_samples_per_rank = defaultdict(list)
    rank_flags = {rank: False for rank in players_per_rank}  # Flag to track if 2500 valid samples are reached for each rank

    def __init__(self):
        options = Options()
        self.driver = webdriver.Firefox(options=options)
        self.consecutive_errors = 0  # Keep track of consecutive errors

    def adjust_delay(self):
        # Calculate exponential backoff
        delay = min(0.5 * (2 ** self.consecutive_errors), 60)
        # Add jitter: random value between 0 and delay
        jitter = random.uniform(0, delay)
        self.custom_settings['DOWNLOAD_DELAY'] = delay + jitter

    def start_requests(self):
        self.driver.get("https://www.streetfighter.com/6/buckler")
        input("Press Enter after you've logged in manually...")
        cookies = self.driver.get_cookies()
        cookies_dict = {c['name']: c['value'] for c in cookies}  # Convert cookies into dict
        for rank in self.players_per_rank:
            yield from self.request_rank_pages(rank, cookies_dict)  # Pass cookies dict

    def request_rank_pages(self, rank, cookies):
        start_page, end_page = self.pages_per_rank[rank]
        while len(self.valid_samples_per_rank[rank]) < 2500 and len(self.sampled_pages_per_rank[rank]) < (
                end_page - start_page + 1):
            if self.rank_flags[rank]:
                # If the flag is True, indicating the threshold is reached, stop processing for the current rank
                logging.info(f"Threshold reached for rank {rank}. Skipping remaining pages.")
                return

            page = random.randint(start_page, end_page)
            if page not in self.sampled_pages_per_rank[rank]:
                self.sampled_pages_per_rank[rank].add(page)
                url = f"https://www.streetfighter.com/6/buckler/ranking/league?character_filter=1&character_id=luke&platform=1&user_status=1&home_filter=1&home_category_id=0&home_id=1&league_rank=0&page={page}"
                yield scrapy.Request(url, cookies=cookies, callback=self.parse_page,
                                     headers={'Referer': None},
                                     cb_kwargs={'rank': rank, 'page': page, 'cookies': cookies})

    def parse_page(self, response, rank, page, cookies):
        try:
            json_data = json.loads(response.css('script#__NEXT_DATA__::text').get())
            if 'league_point_ranking' not in json_data['props']['pageProps']:
                self.consecutive_errors += 1  # Increment the error count
                self.adjust_delay()  # Adjust the delay based on the error count
                print(f"No 'league_point_ranking' data found on page {page} for rank {rank}. Skipping to the next page.")
                return
            self.consecutive_errors = 0  # Reset the error count if the page is successfully parsed
            ranking_fighter_list = json_data['props']['pageProps']['league_point_ranking']['ranking_fighter_list']
            for fighter in ranking_fighter_list:
                username = fighter['fighter_banner_info']['personal_info']['short_id']
                character = fighter['character_name']
                url = f"https://www.streetfighter.com/6/buckler/profile/{username}/play"
                yield scrapy.Request(url, cookies=cookies, callback=self.parse,
                                     headers={'Referer': None},
                                     cb_kwargs={"username": username, "rank": rank, "character": character})
            logging.info(f"Parsed page {page} for rank {rank}.")
        except Exception as e:
            logging.error(f"Failed to parse page data for page {page} in rank {rank}: {e}")
            yield scrapy.Request(response.url, dont_filter=True,
                                 cb_kwargs={'rank': rank, 'page': page, 'cookies': cookies})

    def parse(self, response, username, rank, character):
        try:
            script_tag = response.css('script#__NEXT_DATA__::text').get()
            if script_tag is not None:
                json_data = json.loads(script_tag)
                characters_data = json_data['props']['pageProps']['play']['character_win_rates']
                total_battle_stats = json_data['props']['pageProps']['play']['battle_stats']

                ranked_battle_count = total_battle_stats['rank_match_play_count']

                character_data = next(
                    (data for data in characters_data if data['character_name'].lower() == character.lower()), None)

                if character_data is not None and ranked_battle_count >= 90:
                    if character_data['battle_count'] != 0:
                        win_ratio = character_data['win_count'] / character_data['battle_count']
                        scaled_win_count = win_ratio * ranked_battle_count
                    else:
                        win_ratio = 0
                        scaled_win_count = 0

                    self.valid_samples_per_rank[rank].append(
                        [username, rank, character, ranked_battle_count, scaled_win_count])
                    logging.info(f"{rank}: {len(self.valid_samples_per_rank[rank])}/{2500}")
                    if len(self.valid_samples_per_rank[rank]) >= 2500:
                        self.write_to_csv(rank)
                        self.valid_samples_per_rank[rank] = []  # Reset the samples for the rank
                        self.rank_flags[rank] = True  # Set the flag to True for the rank

                    if all(self.rank_flags.values()):
                        # If all rank flags are True, indicating all ranks have reached the threshold, close the spider
                        self.crawler.engine.close_spider(self, "All ranks have reached the threshold")

            logging.info(f"Parsed profile data for user {username}.")
        except Exception as e:
            logging.error(f"Failed to parse profile data for user {username}: {e}")
            yield scrapy.Request(response.url, dont_filter=True,
                                 cb_kwargs={"username": username, "rank": rank, "character": character})

    def write_to_csv(self, rank):
        filename = f"output_{rank}.csv"
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            samples = self.valid_samples_per_rank[rank]
            for sample in samples:
                writer.writerow(sample)

    def close_spider(self, spider):
        for rank in self.valid_samples_per_rank:
            if len(self.valid_samples_per_rank[rank]) > 0:
                self.write_to_csv(rank) 
