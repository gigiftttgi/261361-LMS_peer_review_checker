import requests
import json
import csv
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
# assessor = []
# assessor_id = []
# asset_id = []
# AssessorAndScore = []
# score = []
# aas_all = []
# row_list = []
n_peerreview = peerreview.ureview
n_assessments = assesments.assessments

# for i in range(len(n_peerreview)):
#     if n_peerreview[i]['user_id'] in userid:
#         assessor_id.append(n_peerreview[i]['assessor_id'])
#         if len(assessor_id)%3 == 0:
#             assessor.append(assessor_id)
#             assessor_id = []
#     else:
#         userid.append(n_peerreview[i]['user_id'])
#         username.append(requests.get(URL+'users/'+ str(n_peerreview[i]['user_id']) ,headers = {'Authorization': 'Bearer ' + TOKEN}).json()['name'])
#         assessor_id.append(n_peerreview[i]['assessor_id'])
#         asset_id.append(n_peerreview[i]['asset_id'])
    # print(i , ' ', 'ass_id: ', assessor_id, ' ', 'ass: ', assessor)
# print(assessor)
# print(asset_id)

# for i in range(len(asset_id)):
#     for j in range(len(n_assessments)):
#         if asset_id[i] == n_assessments[j]['artifact_id'] and assessor[i][0] == n_assessments[j]['assessor_id']:
#             score.append(n_assessments[j]['assessor_id'])
#             score.append(n_assessments[j]['score'])
#             AssessorAndScore.append(score)
#             score = []
#             # if len(AssessorAndScore)%3 == 0:
#             #     aas_all.append(AssessorAndScore)
#             #     AssessorAndScore = []

#         elif asset_id[i] == n_assessments[j]['artifact_id'] and assessor[i][1] == n_assessments[j]['assessor_id']:
#             score.append(n_assessments[j]['assessor_id'])
#             score.append(n_assessments[j]['score'])
#             AssessorAndScore.append(score)
#             score = []
#             # if len(AssessorAndScore)%3 == 0:
#             #     aas_all.append(AssessorAndScore)
#             #     AssessorAndScore = []

#         elif asset_id[i] == n_assessments[j]['artifact_id'] and assessor[i][2] == n_assessments[j]['assessor_id']:
#             score.append(n_assessments[j]['assessor_id'])
#             score.append(n_assessments[j]['score'])
#             AssessorAndScore.append(score)
#             score = []
#             # if len(AssessorAndScore)%3 == 0:
#             #     aas_all.append(AssessorAndScore)
#             #     AssessorAndScore = []

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


fields = ['Name', 'Assignment id', 'Name review 1', 'Review score 1', 'Name review 2', 'Review score 2', 'Name review 3', 'Review score 3']

with open('worksheet.csv', 'w', newline='') as file:
    # w = csv.DictWriter(file, fieldnames = fields)
    # w.writeheader()
    w = csv.writer(file)
    w.writerow(fields)
    for i in range(len(userid)):
        w.writerow([username[i], '11301', a1name[i], s1[i], a2name[i], s2[i], a3name[i], s3[i]])
