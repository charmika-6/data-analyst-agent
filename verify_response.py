# verify_response.py
import requests, base64, json

r = requests.post("http://127.0.0.1:8000/api/", files={"file": open("question.txt","rb")})
print("status:", r.status_code)
resp = r.json()
print("response (first 3 items):", resp[:3])
assert isinstance(resp, list), "Response must be a JSON array"
assert len(resp) == 4, "Response must have 4 elements"
assert isinstance(resp[0], int), "1st element should be integer"
assert isinstance(resp[1], str), "2nd element should be string"
assert isinstance(resp[2], float) or isinstance(resp[2], int), "3rd should be numeric"
assert isinstance(resp[3], str) and resp[3].startswith("data:image/"), "4th should be image data URI"
print("Basic checks passed.")
# Optionally write full JSON to file:
open("output/last_response.json","w",encoding="utf8").write(json.dumps(resp))
