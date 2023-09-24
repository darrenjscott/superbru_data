##############################################
# Temporary file for learning scraping
##############################################

import requests
from bs4 import BeautifulSoup

# Download the HTML document
response = requests.get("https://scrapeme.live/shop")

# Check whether this worked or not
if response.ok:
    # Scraping logic in case of 2xx
    pass
else:
    # Log error response
    # in case of 4xx or 8xx
    print(response)

# Print the HTML code
#print(response.text)

# Parse the HTML with BeautifulSoup
# Note, we use .content rather than .text here
# since .content holds the html data in raw bytes
# rather than a string, which might be tricky to work with
soup = BeautifulSoup(response.content, "html.parser")

price_find = soup.find(class_='woocommerce-Price-amount amount')

# Since pages change overtime, make sure .find actually found something
# It returns None if it doesn't find anything
if price_find is not None:
    print(price_find)