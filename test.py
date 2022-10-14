import requests

url = "https://api.apilayer.com/exchangerates_data/convert?to=GBP&from=INR&amount=8000"

payload = {}
headers= {
  "apikey": "hSBA6NHxu7IDTjKA7RvaA6oFiny5PyE7"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.json()

print(result["query"]["amount"], end = ' ')
print(result["query"]["from"], end = ' ')
print("is equal to", end = ' ')
print(result["result"], end = ' ')
print(result["query"]["to"], end = ' ')
