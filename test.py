import requests

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

# create data
response = requests.put(BASE + "review/1", json=data1)
print("review 1 created")
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
print("review 2 created")

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
print("review 3 created")

input()

# find data
response = requests.get(BASE + "review/1")
print("review 1 found.")
print(response.json())

input()

response = requests.get(BASE + "review/3")
print("review 3 found.")
print(response.json())

input()

response = requests.delete(BASE + "review/2")
print("review 2 deleted")
print(response)