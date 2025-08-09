from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_wikipedia
from analyzer import analyze_data
from plotter import plot_data
import os

app = FastAPI()

class AnalysisRequest(BaseModel):
    topic: str
    question: str

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    try:
        # Step 1: Scrape Wikipedia data
        data = scrape_wikipedia(request.topic)

        # Step 2: Analyze data
        analysis_result = analyze_data(data, request.question)

        # Step 3: Generate plot (if applicable)
        plot_path = plot_data(data, request.topic)

        return {
            "topic": request.topic,
            "question": request.question,
            "analysis": analysis_result,
            "plot_path": plot_path if plot_path else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
