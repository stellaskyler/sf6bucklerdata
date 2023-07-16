# Street Fighter Spider

Street Fighter Spider is a Python web scraper based on Scrapy that scrapes the Street Fighter gaming site for player data. It uses Selenium for dealing with JavaScript and to control the flow of the application.

## Requirements

This project requires Python 3.7+ and the following Python libraries installed:

- Scrapy
- Selenium
- json
- csv
- collections
- logging

You will also need to have Firefox installed on your machine, as the project uses the Firefox webdriver for Selenium.

## Project Structure

The project consists of three main Python files:

- `main.py`
- `spiders/middlewares.py`
- `spiders/street_fighter_spider.py`

`main.py` is the main script that configures and starts a Scrapy process with the `StreetFighterSpider` spider.

`spiders/middlewares.py` contains two middleware classes: `RandomUserAgentMiddleware` and `RetryChangeProxyMiddleware`.

- `RandomUserAgentMiddleware` sets a random User-Agent for each request to help avoid getting blocked by the site.
- `RetryChangeProxyMiddleware` handles failed requests and retries them after adjusting the delay.

`spiders/street_fighter_spider.py` contains the `StreetFighterSpider` spider class.

## How the Spider Works

This spider fetches player data and writes it into CSV files. It uses Selenium to handle pages that contain JavaScript and also implements retry logic and request delay adjustment based on consecutive failed requests.

Before the scraper can start, it will open Firefox and navigate to the Street Fighter site. You will need to log in manually, and then press Enter in your terminal to continue.

Please note that the scraper needs to be run from a command-line interface, like Terminal on MacOS or Command Prompt / PowerShell on Windows.

The spider works by first logging into the Street Fighter site and then navigating to different pages to collect player data.

For each rank in the game, it randomly samples pages and fetches player data. It continues sampling pages until it has collected at least 2500 valid samples (i.e., players with a certain number of ranked battles) for each rank.

Once it has collected enough samples for a rank, it writes the data to a CSV file and moves on to the next rank.

If the spider encounters an error while fetching a page, it retries the request with an exponential backoff delay. This helps to handle temporary issues like network errors or server overloads.
Output

The spider writes the scraped data to CSV files. There is a separate file for each rank. The files are named like output_{rank}.csv, where {rank} is the rank of the players in the file.

Each row in the CSV files contains the following fields:

    Username: The player's username
    Rank: The player's rank
    Character: The character used by the player
    Ranked Battle Count: The total number of ranked battles played by the player
    Scaled Win Count: The win count of the player, scaled according to their win ratio and ranked battle count

## Limitations and Considerations

- The scraper is dependent on the structure of the web pages. If the site changes its layout or the way it delivers data, the scraper may stop working.
- The scraper uses a single-threaded model for fetching pages. Although it can handle a high number of requests, it may not be the most efficient method for large-scale scraping.
- The scraper does not use proxies to rotate IP addresses. If the site blocks your IP due to too many requests, you may need to wait a while before running the scraper again.

## How to Run

Before running, update the players_per_rank in the spider to reflect current numbers, check and/or change the user agents, and check/change the output file.

You can run the scraper from your terminal using the following command:

   python main.py

   

## Disclaimer and Liability

Please be advised that this repository is provided for instructional and educational purposes only.

The data scraping practices demonstrated in this repository must be used responsibly and ethically. Always respect the terms of service of any website or online service you interact with. Be aware that improper use of data scraping techniques can violate the terms of service of some websites or even local laws and regulations.

Under no circumstances should the code be used for any illegal or unethical activities. The authors of this repository disclaim all liability for any damage, loss, or consequence caused directly or indirectly by the use or inability to use the information or code contained within this repository.

Please use this code responsibly and consider the potential impact on servers, respect privacy, and adhere to all relevant terms of service and laws. If you choose to use the code provided in this repository, you do so at your own risk.

## License

This project is licensed under the MIT License. This license does not include the right to use this code, or any derivative work thereof, for any illegal or unethical activities. By using or adapting this code, you agree to assume all liability and responsibility for your actions.
