# Data Analyst Agent

A FastAPI-based app that accepts a `.txt` file containing an analysis question, processes it using Python data tools and LLMs, and returns results as JSON.  

**Live API Endpoint:**  
https://data-analyst-agent-1hzk.onrender.com/api/

---

## Features
- Wikipedia scraping (`/test-scrape/`)
- Data analysis from natural language questions
- Visualization generation
- Deployed on Render

---

## Usage
1. Save your question in `question.txt`.
2. Send a `POST` request with the file:
```python
import requests
url = "https://data-analyst-agent-1hzk.onrender.com/api/"
files = {"file": ("question.txt", open("question.txt", "rb"), "text/plain")}
print(requests.post(url, files=files).json())

Locoal setup
git clone https://github.com/<your-username>/data-analyst-agent.git
cd data-analyst-agent
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn main:app --reload

Test locally at
http://127.0.0.1:8000/api/


