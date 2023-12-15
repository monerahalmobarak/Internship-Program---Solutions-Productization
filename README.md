# Oil Price Data Crawling and Updating Interface

# Project Overview

This project consists of two main components:

Data Crawling: A Python script (Data Crawling.py) that crawls oil price data from the website 'http://www.eia.gov'. It uses libraries like requests, BeautifulSoup4, and pandas to extract, process, and store data.

Web Interface for Data Update: An HTML template (update.html) for updating oil price records. This interface allows users to input old and new data regarding oil prices, areas, and dates.

Setup and Installation
Prerequisites
Python 3.x
pip (Python package manager)
PostgreSQL database (for storing crawled data)
Installing Required Python Libraries
Run the following commands to install the necessary libraries:

pip install beautifulsoup4 pandas sqlalchemy psycopg2
Configuring the Database
Set up a PostgreSQL database.
Modify the db_connection_string in Data Crawling.py to match your database credentials.
Running the Data Crawling Script
Execute Data Crawling.py to start the data crawling process. The script will scrape the latest oil price data and store it in the configured database.

Setting Up the Web Interface
Place update.html in your web server's directory.
Ensure that the server is configured to handle the form submission to /update_price.
Usage
Run the Python script to scrape and store data in your database.
Use the web interface to manually update oil price records as needed.
