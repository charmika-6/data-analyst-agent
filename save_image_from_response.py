# save_image_from_response.py
import requests, base64, os
r = requests.post("http://127.0.0.1:8000/api/", files={"file": open("question.txt","rb")})
resp = r.json()
img_data_uri = resp[3]
header, b64 = img_data_uri.split(",", 1)
img_bytes = base64.b64decode(b64)
os.makedirs("output/plots", exist_ok=True)
path = "output/plots/plot_result.png"
with open(path, "wb") as f:
    f.write(img_bytes)
print("Saved to:", path, "size (bytes):", len(img_bytes))
