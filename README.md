# Street Fighter Buckler Data

This Python script is designed to scrape player data from the Street Fighter website. The collected data can be used for a variety of purposes, such as data analysis, machine learning, and statistical modeling.


## Methodology

The aim of this project is to gather a representative sample of player data from each rank category in the Street Fighter player population. The scraper is designed to collect data from 2500 players per rank, ensuring a substantial and diverse dataset.

The scraper determines the number of pages to sample from for each rank category by dividing the total number of players in that rank category by 20 (the number of players listed on each ranking page). The scraper then selects a random set of these pages for data collection, ensuring that the same page is not sampled more than once.

On each sampled page, the scraper collects data from all the players listed. The data includes the player's username, rank, main character, total number of matches played, and win count. The scraper only collects data from players who have played at least 240 matches in total. This threshold was chosen to ensure that the dataset only includes players who have a significant level of experience. The number 240 was derived from the assumption that a player would have enough experience if they had played against each character in the game at least 10 times, which approximates to around 8 hours of playtime.

In cases where consecutive errors occur, such as failed requests due to server issues or network problems, the scraper employs an exponential backoff with jitter strategy. This strategy dynamically increases the delay between requests, helping manage the load on the server and minimizing the risk of the scraper being blocked by the website.

The data collection process continues until the scraper has collected the target number of samples for each rank category. At this point, the data is written to a CSV file and the scraping process terminates.


## How to Run

    Ensure you have Python 3 installed, along with the required packages. The main requirements are Scrapy and Selenium.

    Download the Python script.

    In the script, replace the file path in the close method with the path where you want the output CSV file to be saved.

    In the script, add whatever user agents you want to the Custom Settings. Make sure you have the corresponding browser driver.

    Run the script. When the script opens the Street Fighter website in Firefox, manually log in and press Enter in the console to continue the scraping process.
    

## Output

The script outputs a CSV file containing the scraped player data. Each row represents one player, with columns for username, rank, main character, total number of matches played, and win count.


## Custom Settings

The scraper is configured with several custom settings to optimize the scraping process and handle potential errors. These settings include parameters for retry times, HTTP response codes to retry, download delay, concurrent requests, user agent rotation, and more.

## Disclaimer

Please note that web scraping should be performed in accordance with the terms of service of the website being scraped and any applicable laws. This script is provided for educational purposes only. Always ensure that your web scraping activities are legal and ethical.
