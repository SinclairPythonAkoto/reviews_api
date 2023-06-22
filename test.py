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

# find reviews
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

input()

response = requests.get(BASE + "review/3")
if response.status_code == 302:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
    print(response.json())
else:
    print("Could not find review: ", response.status_code)


# delete review 2 via id
input()
response = requests.delete(BASE + "review/2")
if response.status_code == 204:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
    print(response)
else:
    print("Could not delete review: ", response.status_code)

# update review 1 via id
input()
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

# display all reviews
input()
response = requests.get(BASE + "review/find/all")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not display all reviews:", response.status_code) 


# create new review (without ID)
input()
review_data = {
    "door": "42",
    "street": "Arden road",
    "location": "Crawley",
    "postcode": "RH10 6HL",
    "rating": 2,
    "review": "this is a bad comment",
    "reviewee": "tenant"
}
response = requests.put(BASE + "review/create", json=review_data)
if response.status_code == 201:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not create new review:", response.status_code) 

# find review using review_uid
input()
review_uid = "0a8afa0a-19f3-478a-9ad1-383171578f8a"    # uid from review 4
response = requests.get(BASE + f"review/{review_uid}")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not find reviews with review unique ID:", response.status_code)


# update review using review_uid
input()
review_update = {
    "rating": 4,
    "review": "this is an updated good review ",
    "reviewee": "visitor"
}
response = requests.patch(BASE + f"review/{review_uid}", json=review_update)
if response.status_code == 200:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not update review with review unique ID given:", response.status_code)


# check data
input()
response = requests.get(BASE + "review/find/all")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not display all reviews:", response.status_code) 

# delete review via review_uid
input()
response = requests.delete(BASE + f"review/{review_uid}")
if response.status_code == 204:
    custom_header = response.headers.get("Custom-Header")
    print(custom_header)
else:
    print("Could not delete review with unique ID given: ", response.status_code)

# find review via door number
input()
door = "39"
response = requests.get(BASE + f"review/filter/door/{door}")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not find review:", response.status_code)

# find review via street name
input()
street = "Winning Hill Close"
response = requests.get(BASE + f"review/filter/street/{street}")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not find review:", response.status_code)

# find review via location
input()
location = "Gorton"
response = requests.get(BASE + f"review/filter/location/{location}")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not find review:", response.status_code)


# find review via postcode
input()
postcode = "SW17 0en"
response = requests.get(BASE + f"review/filter/postcode/{postcode}")
if response.status_code == 302:
    try:
        data = response.json()
        print(response.headers.get("Custom-Header"))
        print(data)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error:", str(e))
        print("Response content:", response.text)
else:
    print("Could not find review:", response.status_code)