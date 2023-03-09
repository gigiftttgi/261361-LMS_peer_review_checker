# from flask import Flask,render_template
import os
from flask import Flask,request, render_template, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import statistics as st
import requests
import csv
import json
import asyncio
import peerreview
import assesments



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
loop = asyncio.get_event_loop()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
global ambilist
global badlist
global error
global token
global courseid
global assignid
global rubricid

@app.route('/')
def Home():
   return render_template("home.html")

@app.route('/api')
def API():
   return render_template("api.html")

async def getAssess():
   URL = 'https://mango-cmu.instructure.com/api/v1/courses/'
   # URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/rubrics/2568?include%5B%5D=peer_assessments'
   # TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
   f = open('assesments.py', 'w')
   response = requests.get(URL + courseid + '/rubrics/' + rubricid + '?include%5B%5D=peer_assessments', headers = {'Authorization': 'Bearer ' + token})

   f.write('assessments = [')
   for i in range(len(response.json()['assessments'])):
      f.write(str(response.json()['assessments'][i]) + ',')
   f.write(']')
   f.close()
   return True

async def getReview():
   await getAssess()
   URL = 'https://mango-cmu.instructure.com/api/v1/courses/'
   # URL = 'https://mango-cmu.instructure.com/api/v1/courses/1306/assignments/11301/peer_reviews'
   # TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"
   f = open('peerreview.py', 'w')
   response = requests.get(URL+courseid + '/assignments/' + assignid + '/peer_reviews', headers = {'Authorization': 'Bearer ' + token})

   f.write('ureview = [')
   for i in range(len(response.json())):
      f.write(str(response.json()[i]) + ',')
   f.write(']')
   f.close()
   return True

async def writeToCSV():
    await getReview()
    URL = "https://mango-cmu.instructure.com/api/v1/courses/"
   #  TOKEN = "21123~7IqgzXjHh3oxiQuEE1E6tSB2jyAqhPl4T1EFhGUf3ioNVJ7tXBXaWpUlFk0zQohv"

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
            username.append(requests.get(URL+ courseid + '/' +"users/"+str(i["user_id"]), headers = {'Authorization': 'Bearer ' + token}).json()["name"])
            a1id.append(i["assessor_id"])
            a1name.append(requests.get(URL+ courseid + '/' +"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + token}).json()["name"]) 
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
                a2name[index] = requests.get(URL+ courseid + '/'+"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + token}).json()["name"]
                check[index] = 2
            elif check[index] == 2:
                a3id[index] = i["assessor_id"]
                a3name[index] = requests.get(URL+ courseid + '/'+"users/"+str(i["assessor_id"]), headers = {'Authorization': 'Bearer ' + token}).json()["name"]
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


    fields = ['ID', 'Name', 'Assignment', 'Name reviewer1', 'Review score1', 'Name reviewer2', 'Review score2', 'Name reviewer3', 'Review score3']

    with open('uploads/input.csv', 'w', newline='') as file:
        # w = csv.DictWriter(file, fieldnames = fields)
        # w.writeheader()
        w = csv.writer(file)
        w.writerow(fields)

        for i in range(len(userid)):
            w.writerow([int(userid[i]),username[i], int(assignid), a1name[i], int(s1[i]), a2name[i], int(s2[i]), a3name[i], int(s3[i])])
    return True

@app.route('/fetchapi')
async def FetchAPI():
      render_template("fetch.html")
      a = await writeToCSV()
      return redirect(url_for('Processing'))
      # return jsonify("success")


@app.route('/fetch', methods=['POST'])
async def Fetch():
   global courseid
   global assignid
   global rubricid
   global token
   courseid = request.form['courseid']
   assignid = request.form['assignid']
   rubricid = request.form['rubricid']
   token = request.form['TOKEN']
   # print(courseid)
   # print(assignid)
   # print(rubricid)
   # print(token)
   a = await writeToCSV()
   return redirect(url_for('Processing'))
   # return redirect(url_for('fetchapi'))


# @app.route('/fetchcomplete')
# async def FetchComplete():
#    return redirect(url_for('Processing'))

@app.route('/fetch-error')
async def FetchError():
   return render_template("fetchError.html")

@app.route('/upload')
def Upload():
   return render_template("upload.html")

@app.route('/upload-error')
def UploadError():
   return render_template("uploadError.html")

@app.route('/processing')
def Processing():  
   return render_template("process.html")

# def swap_columns(df, col1, col2):
#     col_list = list(df.columns)
#     x, y = col_list.index(col1), col_list.index(col2)
#     col_list[y], col_list[x] = col_list[x], col_list[y]
#     df = df[col_list]
#     return df

@app.route('/process')
def Process():

   global error

   df  = pd.read_csv("uploads/input.csv")

   df = df.replace('',np.nan)
   dt = {'Name': np.dtype('O'), 'Assignment': np.dtype('int64'), 'Name reviewer1': np.dtype('O'), 'Review score1': np.dtype('int64'),
         'Name reviewer2': np.dtype('O'), 'Review score2': np.dtype('int64'), 'Name reviewer3': np.dtype('O'), 'Review score3': np.dtype('int64')}

   #csv issues
   if (df.isnull().sum().sum() != 0):
      error = "missing"
      return jsonify("process-error-mising")

   ambi = []
   sus = []
   bad = []
   global badlist
   global ambilist

   att = ['Name', 'Assignment', 'Name reviewer1', 'Review score1', 'Name reviewer2', 'Review score2', 'Name reviewer3', 'Review score3']
   in_att = list(df.columns)



   if (att == in_att and dict(df.dtypes) == dt) :
      dfd = df.drop(['Name','Assignment','Name reviewer1','Name reviewer2','Name reviewer3'], axis='columns')

      for i in range(0,len(dfd)):
      #sort
         dfS = []
         dfS.append(dfd.iloc[i][0])
         dfS.append(dfd.iloc[i][1])
         dfS.append(dfd.iloc[i][2])
         dfS.sort(reverse=True)

         a = dfS[0] - dfS[1]
         b = dfS[1] - dfS[2]
    
         if 1 >= abs(a-b) >= 0:
            if st.stdev(dfS)>1.6:   #find ambigious
               ambi.append(df.iloc[i])
         elif (a+b) >=3:     #still improving
            sus.append(df.iloc[i])      #find sus
            if a>b :
               bad.append(dfS[0])
            elif b>a:
               bad.append(dfS[2])

      ambi = pd.DataFrame(ambi)
      sus = pd.DataFrame(sus)


      # list of ambigious review to display in the table. 
      if(ambi.empty):
         ambilist = ""
      else :
         ambilist = ambi.to_json(orient="values")

      #write csv
      ambi.to_csv('ambigious.csv', index=False)
      if(sus.empty):
         badlist = ""
         return jsonify("processing")
      
      sus.to_csv('suspect.csv', index=False)

      #read sus.csv
      sus  = pd.read_csv("suspect.csv")

      #Map bad from sus.csv
      name = []
      asn = []
      bname = []
      bscore = []
      for i in range(len(sus)):
         name.append(sus.iloc[i]['Name'])
         asn.append(sus.iloc[i]['Assignment'])
         if(sus.iloc[i]['Review score3'] == bad[i] ):
            bname.append(sus.iloc[i]['Name reviewer3'])
            bscore.append(sus.iloc[i]['Review score3'])
         elif(sus.iloc[i]['Review score2'] == bad[i]):
            bname.append(sus.iloc[i]['Name reviewer2'])
            bscore.append(sus.iloc[i]['Review score2'])  
         elif(sus.iloc[i]['Review score1'] == bad[i]):
            bname.append(sus.iloc[i]['Name reviewer1'])
            bscore.append(sus.iloc[i]['Review score1'])

      # bad_review = {
      #    'Name' : name,
      #    'Assignment' : asn,
      #    'Bad Reviewer' : bname,
      #    'Score' : bscore
      # }

      bad_review = {
         'Bad Reviewer' : bname,
         'Score' : bscore,
         'Name' : name,
         'Assignment' : asn
      }

      bad = pd.DataFrame(bad_review)

      badlist = bad.to_json(orient="values")

      bad.to_csv('bad_reviewer.csv', index=False)

      return jsonify("processing")
   else :
      error = "att"
      return jsonify("process-error-att")
   

@app.route('/processing-error')
def ProcessError():
   return render_template("processError.html", error = error)

@app.route('/result')
def Result():
   global badlist
   global ambilist
   return render_template("result.html", ambiresult = ambilist, badresult = badlist)


def allowed_file(filename):
   return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
      f = request.files['filename']
      if f and allowed_file(f.filename) :
         f.save(os.path.join (app.config['UPLOAD_FOLDER'],"input.csv"))
         return redirect(url_for('Processing'))
      else :
         return redirect(url_for('UploadError'))
    else: return redirect(url_for('UploadError'))

if __name__ == '__main__':
 app.debug = True
 app.run(host='0.0.0.0', port=8000)