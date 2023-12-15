#!/usr/bin/env python
# coding: utf-8

# In[41]:


get_ipython().system('pip install beautifulsoup4 pandas ')
get_ipython().system('pip install pandas ')
get_ipython().system('pip install sqlalchemy ')
get_ipython().system('pip install psycopg2')


# In[40]:


# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine


# In[16]:


# URL of the website to scrape
url = 'http://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm'

# Send a request to the website
response = requests.get(url)


# In[21]:


def format_date(date_str):
    try:
        # Parse the date assuming it's in "MM/DD/YY" format
        dt = datetime.strptime(date_str, "%m/%d/%y")
        # Return the date in "11 December 2023" format
        return dt.strftime("%d %B %Y")
    except ValueError:
        # If parsing fails, return the original string
        return date_str


# In[22]:


# Check if the request was successful
if response.status_code == 200:
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all header dates and format them
    header_dates = [format_date(header.get_text(strip=True)) for header in soup.find_all('th', class_='Series5')]

    # Initialize lists to store data
    dates = []
    areas = []
    prices = []

    # Loop through each row in the table body
    for row in soup.select('tr.DataRow'):
        # Find the first cell in the row, which contains the area
        area_cell = row.find('td', class_='DataStub1')

        # Skip the row if it doesn't have an area cell
        if not area_cell:
            continue

        # Get the text of the area cell
        area = area_cell.get_text(strip=True)

        # Find all price cells in the row
        price_cells = row.find_all('td', class_='DataB')

        # Loop through each price cell
        for index, cell in enumerate(price_cells):
            # Check if the index is within the range of header_dates
            if index < len(header_dates):
                # Append the date, area, and price to the respective lists
                dates.append(header_dates[index])
                areas.append(area)
                prices.append(cell.get_text(strip=True))

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Date': dates,
        'Area/Product': areas,
        'Price': prices
    })
    
    # Print the DataFrame
    print(df.head(5))
else:
    print("Failed to fetch data from the website.")


# In[23]:


df


# In[37]:


def save_to_database(df, table_name, db_connection_string):
    """
    Saves the DataFrame to the specified PostgreSQL table.
    :param df: DataFrame to save
    :param table_name: Name of the table where data will be saved
    :param db_connection_string: Database connection string
    """
    engine = create_engine(db_connection_string)
    df.to_sql(table_name, engine, if_exists='replace', index=False)

# Database Connection String
# Format: "postgresql://username:password@localhost/dbname"
db_connection_string = 'postgresql://postgres:1234@localhost/sqldatabase'

# Table name in the database
table_name = 'oil_prices'

# Saving DataFrame to the PostgreSQL database
save_to_database(df, table_name, db_connection_string)

