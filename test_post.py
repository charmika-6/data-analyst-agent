import requests

BASE_URL = "http://127.0.0.1:8000"  # or your Render URL when deployed
ENDPOINT = "/api/"  # matches exactly the route in main.py

url = BASE_URL + ENDPOINT

files = {
    "file": ("question.txt", open("question.txt", "rb"), "text/plain")
}

response = requests.post(url, files=files)

print("Status code:", response.status_code)
print("Response:")
print(response.json())

