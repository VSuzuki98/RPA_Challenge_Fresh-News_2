https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-2-0-37e2db5f88cb48d5ab1c972973226eb4
# Fresh-news
Fresh-news is a Python application that scrape news using a pre defined set of words

# Scraping New York Times website
This project uses Python and Selenium library to scrape the New York Times website for news articles. The program allows the user to select a search phrase, category, and date range for the articles they want to retrieve. The data is extracted and saved to a Excel file.
Prerequisites

This program requires Python and the following libraries:

    RPA Framework
    Selenium
    Robocorp

The program can be run on any operating system that supports Python.

#Getting Started

To use this program, follow these steps:

    Install the prerequisites using pip or any other package manager
    When you need to run locally, check the payload in the file path 'devdata\work-items-in\data.json'
    Run the 'main.py' file with Python

How to use

If you need to run in Control Room from Robocorp, insert the sample Payload below in tab "Advanced Settings -> Start proccess with input data".
```
{
  "url": "https://www.nytimes.com/",
  "search_phrase": "technology",
  "number_of_months": 1,
  "category": [
    "Arts",
    "Books"
  ]
}
```
OBS: You can change the values from the 'searh_phrase', 'number_of_months' and 'categoory' variables
