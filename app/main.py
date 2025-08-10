# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from .scraper import scrape_wikipedia, OUTPUT_FILE
from .analyzer import analyze_data
import pandas as pd
import os

app = FastAPI(title="Data Analyst Agent")


@app.get("/")
def root():
    return {"message": "Data Analyst Agent API is running"}


@app.get("/test-scrape/")
def test_scrape():
    """
    Scrape and save CSV; return a small preview.
    """
    try:
        df = scrape_wikipedia(save_csv=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    preview = df.head(10).to_dict(orient="records")
    return {"message": f"Scraped and saved to {OUTPUT_FILE}", "preview_rows": preview}


@app.post("/api/")
async def analyze_file(file: UploadFile = File(...)):
    """
    Accepts a file (question.txt) and returns the 4-element JSON array.
    """
    content = await file.read()
    try:
        question_text = content.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode uploaded file. Use UTF-8 text.")

    try:
        result = analyze_data(question_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
