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

`spiders/street_fighter_spider.py` contains the `StreetFighterSpider` spider class. This spider fetches player data and writes it into CSV files. It uses Selenium to handle pages that contain JavaScript and also implements retry logic and request delay adjustment based on consecutive failed requests.

## How to Run

You can run the scraper from your terminal using the following command:

```shell
python main.py
