import requests
import json

URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/rubrics/2568?include%5B%5D=peer_assessments'
TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
f = open('assesments.py', 'a')
response = requests.get(URL, headers = {'Authorization': 'Bearer ' + TOKEN})
print(response.json())
f.write('assessments = [')
for i in range(len(response.json()['assessments'])):
    f.write(str(response.json()['assessments'][i]) + ',')
    print(type(response.json()['assessments'][i]))
f.write(']')
f.close()

# def jprint(obj):
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

