# Street Fighter Data Analysis

This project scrapes Street Fighter player data and performs statistical analysis to investigate the distribution of player skills across various ranks.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download Python from here: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installing

1. Clone this repository to your local machine. You can do this by running the following command in your terminal:

   ```bash
   git clone [https://github.com/stellaskyler/sf6bucklerdata.git]
   ```

   ```bash
   cd my_scrapy_project
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. You're all set! You can now run the project.

### Running the Project

To run the project, simply run the following command in your terminal:

```bash
python main.py
```

This command starts the `CrawlerProcess` and begins the scraping and analysis.

## Project Structure

The project is organized into several files:

- `main.py`: This is the entry point of the project. It starts the `CrawlerProcess`.
- `spiders/street_fighter_spider.py`: This file contains the `StreetFighterSpider` class which defines the scraping logic.
- `middlewares.py`: This file contains the `RandomUserAgentMiddleware` and `RetryChangeProxyMiddleware` classes, which handle rotation of user agents and retrying of requests with a different proxy.
- `requirements.txt`: This file lists the Python packages that the project depends on.

## Methodology

The project begins by scraping data from the Street Fighter ranking pages. For each rank, it randomly selects pages and scrapes data for all players listed on these pages. It then visits each player's profile page to get more detailed data, such as the number of matches played and the number of wins.

The data is then filtered to exclude players who have played less than 240 matches. This is to ensure that the data is statistically significant.

The filtered data is then analyzed to calculate the win rate for each player. This data is then used to investigate the distribution of player skills across various ranks.
