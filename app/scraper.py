import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_highest_grossing_films(url: str) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find first table
    table = soup.find("table", {"class": "wikitable"})
    df = pd.read_html(str(table))[0]
    return df
