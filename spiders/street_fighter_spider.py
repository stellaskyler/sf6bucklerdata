# The main spider class
class StreetFighterSpider(scrapy.Spider):
    name = "street_fighter_spider"

    # Custom settings for the spider
    custom_settings = {
        'RETRY_TIMES': 5,  # The number of times to retry a request if it fails
        'RETRY_HTTP_CODES': [403, 401, 429],  # The HTTP response codes that should trigger a retry
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            '__main__.RetryChangeProxyMiddleware': 540,
            '__main__.RandomUserAgentMiddleware': 400,
        },
        'DOWNLOAD_DELAY': 0.5,  # The initial delay between requests (in seconds)
        'CONCURRENT_REQUESTS': 32,  # The maximum number of concurrent requests
        'AUTOTHROTTLE_ENABLED': True,  # Whether to enable the AutoThrottle extension
        'AUTOTHROTTLE_START_DELAY': 0.5,  # The initial delay for AutoThrottle
        'AUTOTHROTTLE_MAX_DELAY': 60,  # The maximum delay for AutoThrottle
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # The target concurrency level for AutoThrottle
        'USER_AGENTS': [  # A list of user agents to use for requests
            # Various user agents...
        ],
        'AUTOTHROTTLE_DEBUG': False,  # Whether to enable debugging for AutoThrottle
    }

    # The number of players in each rank
    players_per_rank = {'i': 195737, 'b': 210459, 's': 256991, 'g': 202144, 'p': 238252, 'd': 42064, 'm': 1010}

    # The number of pages for each rank
    pages_per_rank = {rank: players // 20 for rank, players in players_per_rank.items()}

    # The pages that have been sampled for each rank
    sampled_pages_per_rank = {rank: set() for rank in players_per_rank.keys()}

    # The valid samples for each rank
    valid_samples_per_rank = defaultdict(list)

    def __init__(self):
        options = Options()
        self.driver = webdriver.Firefox(options=options)  # Initialize the webdriver
        self.consecutive_errors = 0  # Initialize the error counter

    def start_requests(self):
        # Open the website and ask the user to manually log in
        self.driver.get("https://www.streetfighter.com/6/buckler")
        input("Press Enter after you've logged in manually...")
        cookies = self.driver.get_cookies()  # Get the cookies
        cookies_dict = {c['name']: c['value'] for c in cookies}  # Convert cookies into dict

        # Start requesting pages for each rank
        for rank in self.players_per_rank.keys():
            yield from self.request_rank_pages(rank, cookies_dict)

    def request_rank_pages(self, rank, cookies):
        # Request pages for a specific rank until enough valid samples have been collected
        while len(self.valid_samples_per_rank[rank]) < 2500 and len(self.sampled_pages_per_rank[rank]) < self.pages_per_rank[rank]:
            page = random.randint(1, self.pages_per_rank[rank] + 1)  # Select a random page
            if page not in self.sampled_pages_per_rank[rank]:
                self.sampled_pages_per_rank[rank].add(page)  # Mark the page as sampled
                # Construct the URL for the page
                url = f"https://www.streetfighter.com/6/buckler/ranking/league?character_filter=2&character_id=luke&platform=1&user_status=1&home_filter=1&home_category_id=0&home_id=1&league_rank=0&page={page}"
                # Yield a request for the page
                yield scrapy.Request(url, cookies=cookies, callback=self.parse_page, headers={'Referer': None}, cb_kwargs={'rank': rank, 'page': page, 'cookies': cookies})

    def parse_page(self, response, rank, page, cookies):
        # Parse a ranking page
        json_data = json.loads(response.css('script#__NEXT_DATA__::text').get())
        if 'league_point_ranking' not in json_data['props']['pageProps']:
            self.consecutive_errors += 1  # Increment the error count
            self.adjust_delay()  # Adjust the delay
            print(f"No 'league_point_ranking' data found on page {page} for rank {rank}. Skipping to the next page.")
            return
        self.consecutive_errors = 0  # Reset the error count
        ranking_fighter_list = json_data['props']['pageProps']['league_point_ranking']['ranking_fighter_list']
        # Yield a request for each player on the page
        for fighter in ranking_fighter_list:
            username = fighter['fighter_banner_info']['personal_info']['short_id']
            url = f"https://www.streetfighter.com/6/buckler/profile/{username}/play"
            yield scrapy.Request(url, cookies=cookies, callback=self.parse, headers={'Referer': None}, cb_kwargs={"username": username, "rank": rank})

    def parse(self, response, username, rank):
        # Parse a player's page
        script_tag = response.css('script#__NEXT_DATA__::text').get()
        if script_tag is None:
            print(f"No data found for user. Retrying...")
            yield scrapy.Request(response.url, dont_filter=True, cb_kwargs={"username": username, "rank": rank})
        else:
            json_data = json.loads(script_tag)
            characters_data = json_data['props']['pageProps']['play']['character_win_rates']
            characters = [
                {
                    'name': char_data['character_name'],
                    'matches_played': char_data['battle_count'],
                    'win_count': char_data['win_count'],
                }
                for char_data in characters_data
                if char_data['character_name'].lower() not in ['any', 'random']
            ]
            main_character = max(characters, key=lambda x: x['matches_played'])
            # Check if the player has enough matches played
            if main_character['matches_played'] < 240:
                print(f"Skipping user {username} due to insufficient matches played.")
                return
            # Add the player to the valid samples
            self.valid_samples_per_rank[rank].append([username, rank, main_character['name'], main_character['matches_played'], main_character['win_count']])
            print(f"{rank}: {len(self.valid_samples_per_rank[rank])}/{2500}")
            if len(self.valid_samples_per_rank[rank]) >= 2500:
                return

    def adjust_delay(self):
        # Adjust the delay based on the number of consecutive errors
        delay = min(0.5 * (2 ** self.consecutive_errors), 60)  # Calculate the exponential backoff
        jitter = random.uniform(0, delay)  # Calculate the jitter
        self.custom_settings['DOWNLOAD_DELAY'] = delay + jitter  # Set the new delay

    def close(self, reason):
        # Write the data to a CSV file when the spider is closed
        with open('output.csv', 'w', newline='') as file:  # Replace 'output.csv' with the path where you want the file to be saved
            writer = csv.writer(file)
            for rank_samples in self.valid_samples_per_rank.values():
                for sample in rank_samples:
                    writer.writerow(sample)
        self.driver.quit()