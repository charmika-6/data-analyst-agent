from fastapi import FastAPI, File, UploadFile
import uvicorn
#temporary
from app.scraper import scrape_highest_grossing_films
#temp close

app = FastAPI()

@app.post("/api/")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    # Placeholder logic
    print("Received prompt:", text)

    return [
        1,
        "Titanic",
        0.485782,
        "data:image/png;base64,abc123=="  # dummy image
    ]

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

#temp
@app.get("/test-scrape/")
def test_scrape():
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    df = scrape_highest_grossing_films(url)
    return df.head(3).to_dict()
#temp close