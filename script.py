"""
Scrapes headlines from different sections of The Daily Pennsylvanian website 
and saves them to a JSON file that tracks headlines over time.
"""

import os
import sys
from typing import Dict, List, Tuple

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point() -> Dict[str, str]:
    """
    Scrapes headlines from different sections of The Daily Pennsylvanian home page.

    Returns:
        Dict[str, str]: A dictionary mapping section names to their headlines.
    """
    req = requests.get("https://www.thedp.com")
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    headlines = {}
    
    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        
        # Main headline
        main_headline = soup.find("a", class_="frontpage-link")
        if main_headline:
            headlines["main"] = main_headline.text.strip()
        
        # News section headlines
        news_section = soup.find("div", class_="section-news")
        if news_section:
            news_headline = news_section.find("a", class_="article-link")
            if news_headline:
                headlines["news"] = news_headline.text.strip()
        
        # Sports section headlines
        sports_section = soup.find("div", class_="section-sports")
        if sports_section:
            sports_headline = sports_section.find("a", class_="article-link")
            if sports_headline:
                headlines["sports"] = sports_headline.text.strip()
        
        # Opinion section headlines
        opinion_section = soup.find("div", class_="section-opinion")
        if opinion_section:
            opinion_headline = opinion_section.find("a", class_="article-link")
            if opinion_headline:
                headlines["opinion"] = opinion_headline.text.strip()
        
        # Most read article
        most_read = soup.find("div", class_="most-read")
        if most_read:
            most_read_headline = most_read.find("a", class_="article-link")
            if most_read_headline:
                headlines["most_read"] = most_read_headline.text.strip()
        
        loguru.logger.info(f"Scraped headlines: {headlines}")
        return headlines
    
    return headlines


if __name__ == "__main__":
    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        headlines = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        headlines = None

    # Save data
    if headlines is not None:
        for section, headline in headlines.items():
            dem.add_today(f"{section}: {headline}")
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
