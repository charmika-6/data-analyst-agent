# app/scraper.py
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "highest_grossing_films.csv")


def scrape_wikipedia(save_csv: bool = True) -> pd.DataFrame:
    """
    Scrape the Wikipedia 'List of highest-grossing films' table.
    Returns a DataFrame and (optionally) saves it to OUTPUT_FILE.
    """
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    tables = soup.find_all("table", class_="wikitable")

    for table in tables:
        try:
            df = pd.read_html(StringIO(str(table)))[0]
        except Exception:
            continue

        cols_lower = [str(c).lower() for c in df.columns.astype(str)]
        if any("rank" in c for c in cols_lower) and any("worldwide" in c for c in cols_lower):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            if save_csv:
                df.to_csv(OUTPUT_FILE, index=False)
            return df

    raise RuntimeError("Could not find the highest-grossing films table on the page")

