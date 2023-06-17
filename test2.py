import requests
import json

BASE = "http://127.0.0.1:5000/"

# create data object
data1 = {
    "door": "39",
    "street": "Khama road",
    "postcode": "sw17 0en",
    "rating": 4,
    "review": "this is the first review",
    "reviewee": "tenant"
}

# create data via api request
response = requests.put(BASE + "review/1", json=data1)
print(response.json())
input()

# find data via api response
response = requests.get(BASE + "review/1")
print(response.json())

