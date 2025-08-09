# app/plotter.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64


def plot_regression(df: pd.DataFrame, x_col: str, y_col: str) -> str:
    """
    Returns a base64 data URI (PNG) of a scatterplot x_col vs y_col
    with a dotted red regression line. If not enough data, returns empty string.
    """
    df = df.copy()
    # convert to numeric safely
    df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=[x_col, y_col])

    if df.shape[0] < 2:
        return ""

    plt.figure(figsize=(6, 4))
    plt.scatter(df[x_col], df[y_col], alpha=0.7)
    plt.xlabel(x_col)
    plt.ylabel(y_col)

    # regression
    z = np.polyfit(df[x_col], df[y_col], 1)
    p = np.poly1d(z)
    # dotted red regression line
    plt.plot(df[x_col], p(df[x_col]), linestyle="--", color="red", linewidth=1)

    buf = io.BytesIO()
    plt.tight_layout()
    # lower DPI helps keep file size down
    plt.savefig(buf, format="png", dpi=80, bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img_bytes = buf.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"
