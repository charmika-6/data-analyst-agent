# app/analyzer.py
import os
import re
import pandas as pd
from typing import List, Any

from .scraper import scrape_highest_grossing_films, OUTPUT_FILE
from .plotter import plot_regression


def _find_col(df: pd.DataFrame, keyword: str):
    """Return first column name containing keyword (case-insensitive) or None."""
    for c in df.columns:
        if keyword.lower() in str(c).lower():
            return c
    return None


def _clean_gross_series(s: pd.Series) -> pd.Series:
    """Remove non-numeric chars and convert to float safely."""
    return (
        s.astype(str)
         .str.replace(r"[^0-9.]", "", regex=True)
         .replace("", "0")
         .astype(float)
    )


def analyze_data(question_text: str) -> List[Any]:
    """
    Given the text of the question, returns a list of 4 items:
    [count_2bn_before_2020 (int),
     earliest_film_over_1_5bn (str),
     correlation_rank_peak (float),
     image_data_uri (str)]
    """

    # Ensure CSV exists; if not, scrape and save it
    if not os.path.exists(OUTPUT_FILE):
        df = scrape_highest_grossing_films(save_csv=True)
    else:
        df = pd.read_csv(OUTPUT_FILE)

    # Detect column names flexibly
    gross_col = _find_col(df, "worldwide") or _find_col(df, "gross")
    rank_col = _find_col(df, "rank")
    peak_col = _find_col(df, "peak") or _find_col(df, "peak position") or _find_col(df, "peak (weekly)") 
    year_col = _find_col(df, "year")
    title_col = _find_col(df, "title") or _find_col(df, "film") or _find_col(df, "movie")

    # fallbacks: if something not found, try common names
    if gross_col is None:
        # try exact 'Worldwide gross'
        if "Worldwide gross" in df.columns:
            gross_col = "Worldwide gross"

    # Prepare cleaned columns safely
    if gross_col:
        df["gross_clean"] = _clean_gross_series(df[gross_col])
    else:
        df["gross_clean"] = 0.0

    if rank_col:
        df[rank_col] = pd.to_numeric(df[rank_col], errors="coerce")
    if peak_col:
        df[peak_col] = pd.to_numeric(df[peak_col], errors="coerce")
    if year_col:
        df[year_col] = pd.to_numeric(df[year_col], errors="coerce")

    # Default results (so we always return 4 elements)
    count_2bn_before_2020 = 0
    earliest_film = ""
    corr_rank_peak = 0.0
    image_uri = ""

    q = question_text.lower()

    # 1) How many $2 bn movies were released before 2020?
    if ("2 bn" in q) or ("$2" in q) or ("2bn" in q):
        if year_col:
            count_2bn_before_2020 = int(df[(df["gross_clean"] >= 2_000_000_000) & (df[year_col] < 2020)].shape[0])
        else:
            count_2bn_before_2020 = int(df[df["gross_clean"] >= 2_000_000_000].shape[0])

    # 2) Earliest film that grossed over $1.5 bn
    if ("1.5" in q) or ("1.5 bn" in q) or ("1.5bn" in q):
        over = df[df["gross_clean"] >= 1_500_000_000]
        if not over.empty and year_col and title_col:
            try:
                earliest_film = str(over.sort_values(year_col).iloc[0][title_col])
            except Exception:
                earliest_film = str(over.iloc[0][title_col]) if title_col else ""
        elif not over.empty and title_col:
            earliest_film = str(over.iloc[0][title_col])

    # 3) Correlation Rank vs Peak
    if ("correlation" in q) and rank_col and peak_col:
        try:
            corr_val = df[rank_col].corr(df[peak_col])
            corr_rank_peak = float(round(corr_val if pd.notna(corr_val) else 0.0, 6))
        except Exception:
            corr_rank_peak = 0.0

    # 4) Scatterplot of Rank and Peak with dotted red regression line
    if ("scatterplot" in q) or ("scatter plot" in q) or ("scatter" in q):
        if rank_col and peak_col:
            image_uri = plot_regression(df, x_col=rank_col, y_col=peak_col)

    # Ensure types
    if earliest_film is None:
        earliest_film = ""

    return [
        int(count_2bn_before_2020),
        str(earliest_film),
        float(corr_rank_peak),
        str(image_uri),
    ]
