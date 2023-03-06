import requests
import json

URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/assignments/11301/peer_reviews'
TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
f = open('peerreview.py', 'a')
response = requests.get(URL, headers = {'Authorization': 'Bearer ' + TOKEN})

f.write('ureview = [')
for i in range(len(response.json())):
    f.write(str(response.json()[i]) + ',')
f.write(']')
f.close()
