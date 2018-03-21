# Walmart Coupons
Walmart Web Scraper written in Python 3 to extract coupon details for a store location. If you would like to know more about this scraper
you can check it out at the blog post 'How to Scrape Coupons from Walmart using Python 3'

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Fields to Extract
1. Discounted Price
2. Category
3. Brand
4. Product Description
5. Activated Date
6. Expired Date
7. URL

### Prerequisites
For this web scraping tutorial usng Python 3, we will need some some packages:

* Python Requests
* LXML
* UnicodeCSV

### Installation

PIP to install the following packages in Python (https://pip.pypa.io/en/stable/installing/)

Python Requests, to make requests and download the HTML content of the pages (http://docs.python-requests.org/en/master/user/install/)

Python LXML, for parsing the HTML Tree Structure using Xpaths (Learn how to install that here – http://lxml.de/installation.html)

## Running the Scraper

We will execute the script to get the coupon details of store ID 2159:

```
python3 walmart_coupon_retriever.py 2159
```

## Sample Output
This will create a CSV file:

[Sample Output](https://raw.githubusercontent.com/scrapehero/walmart-coupons/master/2159_coupons.csv)
