import requests
import json
import csv
import asyncio


async def getAssess():
    URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/rubrics/2568?include%5B%5D=peer_assessments'
    TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
    f = open('assesments.py', 'w')
    response = requests.get(URL, headers = {'Authorization': 'Bearer ' + TOKEN})

    f.write('assessments = [')
    for i in range(len(response.json()['assessments'])):
        f.write(str(response.json()['assessments'][i]) + ',')
    f.write(']')
    f.close()

async def getReview():
    URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/assignments/11301/peer_reviews'
    TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
    f = open('peerreview.py', 'w')
    response = requests.get(URL, headers = {'Authorization': 'Bearer ' + TOKEN})

    f.write('ureview = [')
    for i in range(len(response.json())):
        f.write(str(response.json()[i]) + ',')
    f.write(']')
    f.close()

async def writeToCSV():
    await getReview();
    await getAssess();
    import peerreview
    import assesments
    URL = "https://mango-cmu.instructure.com/api/v1/courses/1306/"
    TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"

    userid = []
    username = []
    a1id = []
    a1name = []
    a2id = []
    a2name = []
    a3id = []
    a3name = []
    s1 = []
    s2 = []
    s3 = []
    check = []
    n_peerreview = peerreview.ureview
    n_assessments = assesments.assessments

    countu = 0
    for i in n_peerreview:
        countu += 1
        if countu%100 == 0:
            print(countu)
        if userid.count(i['user_id']) == 0:
            check.append(1)
            userid.append(i['user_id'])
            username.append(requests.get(URL+"users/"+str(i["user_id"]), headers = {'Authorization': 'Bearer ' + TOKEN}).json()["name"])
            a1id.append(i["assessor_id"])
            a1name.append(requests.get(URL+"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + TOKEN}).json()["name"]) 
            a2id.append(-1)
            a2name.append("xxx")
            a3id.append(-1)
            a3name.append("xxx")
            s1.append(-1)
            s2.append(-1)
            s3.append(-1)
        else:
            index = userid.index(i["user_id"])
            if check[index] == 1:
                a2id[index] = i["assessor_id"]
                a2name[index] = requests.get(URL+"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + TOKEN}).json()["name"]
                check[index] = 2
            elif check[index] == 2:
                a3id[index] = i["assessor_id"]
                a3name[index] = requests.get(URL+"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + TOKEN}).json()["name"]
                check[index] = 3

    for j in n_assessments:
        for i in n_peerreview:
            if j["artifact_id"]==i["asset_id"]:
                index = userid.index(i["user_id"])
                if a1id[index] == j["assessor_id"]:
                    s1[index] = j["score"]
                elif a2id[index] == j["assessor_id"]:
                    s2[index] = j["score"]
                elif a3id[index] == j["assessor_id"]:
                    s3[index] = j["score"]


    fields = ['Name', 'Assignment', 'Name reviewer1', 'Review score1', 'Name reviewer2', 'Review score2', 'Name reviewer3', 'Review score3']

    with open('uploads/input.csv', 'w', newline='') as file:
        # w = csv.DictWriter(file, fieldnames = fields)
        # w.writeheader()
        w = csv.writer(file)
        w.writerow(fields)

        for i in range(len(userid)):
            w.writerow([username[i], 11301, a1name[i], int(s1[i]), a2name[i], int(s2[i]), a3name[i], int(s3[i])])


asyncio.run(writeToCSV())