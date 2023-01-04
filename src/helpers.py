"""
Helper functions for data analyzing
"""
import requests
from bs4 import BeautifulSoup
import re
import time

def fetch(url,i):
    """
    Fetch data from url using requests
    """
    # Make the GET request
    r = requests.get(url + f"&page={i}")

    # Return the response as TEXT
    return r.text

def soupify(text, city):
    """
    Parse HTML text
    """
    # Declare the data list
    data = []

    # Declare the parser
    soup = BeautifulSoup(text, "html.parser")

    # Find all items of value
    items = soup.find_all(class_ = "_3xhWw")

    # Iterate through the items to filter
    for item in items:

        try:
            # Find the SM (Square Meters)
            square_meter = int(re.sub("[^0-9]", "", str(item.find(class_ = "xaK91").select_one("p:nth-of-type(2)"))))
        except ValueError:
            square_meter = None

        # Find the price
        price = int(re.sub("[^0-9]", "", str(item.find(class_ = "_22nMB").text)))

        # Find the percentage change from asking price
        try:
            change = item.find(class_ = "_3O6Ag").text
            if change == "—" or change == "+/-0 %":
                change = 0
            else:
                change_s = change.split(" ")[0]
                if change_s[0] == "+":
                    change = float(change_s[1:])
                elif change_s[0] == "-":
                    change = float(change_s)
        except AttributeError:
            change = 0

        try:
            # Calculate the PSM (Per Square Meter) price
            psm = price / square_meter
        except TypeError:
            psm = None

        # Find the date
        date = str(item.find(class_ = "_1oXGX").select_one("p:nth-of-type(3)").text)

        # Append the object to data list
        data.append({"city": city, "sm": square_meter, "price": price, "psm": psm, "change": change, "date": date})

    return data


def get_data(url):
    """
    Retrieve data from url, parse it and return as ready-to-use data with pandas
    """
    data = []
    for i in range(1,11):

        # Get the HTML TEXT
        html = fetch(url[0], i)

        # Parse it to filter data
        data.extend(soupify(html, url[1]))

        time.sleep(0.01)
        

    # Return formated data
    return data
