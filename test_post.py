import requests
with open("question.txt", "rb") as f:
    r = requests.post("http://127.0.0.1:8000/api/", files={"file": f})
    print(r.status_code)
    print(r.text[:1000])
