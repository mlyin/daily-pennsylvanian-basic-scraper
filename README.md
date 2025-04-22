# Daily Pennsylvanian Headline Scraper

This repository contains a scraper that collects headlines from different sections of The Daily Pennsylvanian website. The scraper runs once per day and stores the results in a JSON file that tracks headlines over time.

## Features

The scraper collects headlines from multiple sections of the Daily Pennsylvanian website:
- Main headline (frontpage-link)
- News section headlines
- Sports section headlines
- Opinion section headlines
- Most read articles

## Scraper Modifications and Approach

### Original Implementation
The original scraper was designed to collect only the main headline from the Daily Pennsylvanian homepage. It used a simple approach:
- Made a single request to the homepage
- Found the main headline using the CSS selector `a.frontpage-link`
- Stored a single headline per day

### Enhanced Implementation
I've enhanced the scraper to collect a more comprehensive set of headlines by:

1. **Expanding Data Collection**: The scraper now collects headlines from multiple sections:
   - Main headline (using the original `frontpage-link` selector)
   - News section headlines (using `div.section-news a.article-link`)
   - Sports section headlines (using `div.section-sports a.article-link`)
   - Opinion section headlines (using `div.section-opinion a.article-link`)
   - Most read articles (using `div.most-read a.article-link`)

2. **Improved Data Structure**: 
   - Changed the return type from a single string to a dictionary mapping section names to headlines
   - Each headline is now tagged with its section (e.g., "main: Headline text")
   - This allows for better analysis of content across different sections

3. **Enhanced Error Handling**:
   - Added type hints for better code maintainability
   - Improved error handling for each section
   - Added more detailed logging

### Reasoning Behind the Approach

1. **Comprehensive Coverage**: By collecting headlines from multiple sections, we can:
   - Analyze content distribution across different sections
   - Track how different types of news (sports, opinion, etc.) change over time
   - Identify trends in what types of content make headlines

2. **Respectful Scraping**: The approach maintains ethical scraping practices by:
   - Making only one request to the homepage (minimizing server load)
   - Respecting the robots.txt file's crawl delay of 10 seconds
   - Only collecting publicly available information

3. **Data Analysis Potential**: The enhanced data structure enables various analyses:
   - Content distribution analysis (e.g., sports vs. news vs. opinion)
   - Headline change frequency by section
   - Most read article trends
   - Temporal patterns in headline changes

4. **Maintainability**: The code is designed to be:
   - Easy to extend for additional sections
   - Well-documented with type hints
   - Robust with proper error handling

## Data Format

The scraped data is stored in a JSON format that looks like:
```json
{
  "2024-3-3": [
    ["2024-03-03 01:41PM", "main: Main headline text"],
    ["2024-03-03 01:41PM", "news: News section headline"],
    ["2024-03-03 01:41PM", "sports: Sports section headline"],
    ["2024-03-03 01:41PM", "opinion: Opinion section headline"],
    ["2024-03-03 01:41PM", "most_read: Most read article headline"]
  ]
}
```

## Ethical Considerations

This scraper is designed with ethical considerations in mind:
1. Respects the website's robots.txt file
2. Implements a crawl delay of 10 seconds (though we only scrape once per day)
3. Only collects publicly available information
4. Does not overload the server with requests

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper:
   ```bash
   python script.py
   ```

## GitHub Actions

The scraper is configured to run automatically once per day using GitHub Actions. The workflow:
1. Runs the scraper
2. Commits any new headlines to the repository
3. Creates a commit with the updated data file

## Contributing

Feel free to submit issues and enhancement requests!
