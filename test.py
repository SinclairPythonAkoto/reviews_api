import requests
import json

BASE = "http://127.0.0.1:5000/"

# Create a dictionary with the request data
data1 = {
    "door": "39",
    "street": "Khama road",
    "postcode": "sw17 0en",
    "rating": 4,
    "review": "this is a random comment",
    "reviewee": "tenant"
}

# create reviews
response = requests.put(BASE + "review/1", json=data1)
if response.status_code == 201:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
else:
    print("Could not create review: ", response.status_code)
input()

data2 = {
    "door": "18",
    "street": "Hengist street",
    "location": "Manchester",
    "postcode": "m18 7el",
    "rating": 5,
    "review": "this is my second comment",
    "reviewee": "visitor"
}
response = requests.put(BASE + "review/2", json=data2)
if response.status_code == 201:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
else:
    print("Could not create review: ", response.status_code)
input()

data3 = {
    "door": "23",
    "street": "Winning Hill Close",
    "location": "Gorton",
    "postcode": "m18 7dy",
    "rating": 3,
    "reviewee": "neighbour"
}
response = requests.put(BASE + "review/3", json=data3)
if response.status_code == 201:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
else:
    print("Could not create review: ", response.status_code)
input()

# find reviews
response = requests.get(BASE + "review/1")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Request failed with status code:", response.status_code)

input()

response = requests.get(BASE + "review/3")
if response.status_code == 302:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
    print(response.json())
else:
    print("Could not find review: ", response.status_code)
input()

# delete review via id
response = requests.delete(BASE + "review/2")
if response.status_code == 204:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
    print(response)
else:
    print("Could not delete review: ", response.status_code)
input()

# update review via id
updated_review = {
    "rating": 5,
    "review": "this is an updated review",
    "reviewee": "visitor"
}
response = requests.patch(BASE + "review/1", json=updated_review)
if response.status_code == 200:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
    print(response.json())
else:
    print("Could not update review: ", response.status_code)

# check if review has been updated
input()
response = requests.get(BASE + "review/1")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Request failed with status code:", response.status_code)
