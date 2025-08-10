# app/analyzer.py
import os
import pandas as pd
from typing import List, Any

from .scraper import scrape_wikipedia, OUTPUT_FILE
from .plotter import plot_regression


def _find_col(df: pd.DataFrame, keyword: str):
    for c in df.columns:
        if keyword.lower() in str(c).lower():
            return c
    return None


def _clean_gross_series(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
         .str.replace(r"[^0-9.]", "", regex=True)
         .replace("", "0")
         .astype(float)
    )


def analyze_data(question_text: str) -> List[Any]:
    """
    Input: text of question (string)
    Output: list [int, str, float, str(datauri)]
    """
    # ensure CSV exists
    if not os.path.exists(OUTPUT_FILE):
        df = scrape_wikipedia(save_csv=True)
    else:
        df = pd.read_csv(OUTPUT_FILE)

    # detect columns
    gross_col = _find_col(df, "worldwide") or _find_col(df, "gross")
    rank_col = _find_col(df, "rank")
    peak_col = _find_col(df, "peak") or _find_col(df, "peak position")
    year_col = _find_col(df, "year")
    title_col = _find_col(df, "title") or _find_col(df, "film") or _find_col(df, "movie")

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

    # defaults
    count_2bn_before_2020 = 0
    earliest_film = ""
    corr_rank_peak = 0.0
    image_uri = ""

    q = question_text.lower()

    # 1) $2bn movies before 2020
    if ("2 bn" in q) or ("$2" in q) or ("2bn" in q):
        if year_col:
            count_2bn_before_2020 = int(df[(df["gross_clean"] >= 2_000_000_000) & (df[year_col] < 2020)].shape[0])
        else:
            count_2bn_before_2020 = int(df[df["gross_clean"] >= 2_000_000_000].shape[0])

    # 2) earliest > $1.5bn
    if ("1.5" in q) or ("1.5 bn" in q) or ("1.5bn" in q):
        over = df[df["gross_clean"] >= 1_500_000_000]
        if not over.empty and year_col and title_col:
            earliest_film = str(over.sort_values(year_col).iloc[0][title_col])
        elif not over.empty and title_col:
            earliest_film = str(over.iloc[0][title_col])

    # 3) correlation
    if ("correlation" in q) and rank_col and peak_col:
        corr_val = df[rank_col].corr(df[peak_col])
        corr_rank_peak = float(round(corr_val if pd.notna(corr_val) else 0.0, 6))

    # 4) scatterplot
    if ("scatterplot" in q) or ("scatter plot" in q) or ("scatter" in q):
        if rank_col and peak_col:
            image_uri = plot_regression(df, x_col=rank_col, y_col=peak_col)

    return [
        int(count_2bn_before_2020),
        str(earliest_film or ""),
        float(corr_rank_peak),
        str(image_uri),
    ]

