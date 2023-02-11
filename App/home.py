# from flask import Flask,render_template

import json
import os
from flask import Flask,request, render_template, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
global ambilist
global badlist
global fname

# fileitem = form['fileName']
	
@app.route('/')
def Home():
   return render_template("upload.html")

@app.route('/upload-error')
def UploadError():
   return render_template("uploadError.html")

@app.route('/processing')
def Processing():  
   return render_template("process.html")

@app.route('/process')
def Process():

   df  = pd.read_csv("uploads/input.csv")

   ambi = []
   sus = []
   bad = []

   att = ['Name', 'Assignment', 'Name reviewer1', 'Review score1', 'Name reviewer2', 'Review score2', 'Name reviewer3', 'Review score3']
   in_att = list(df.columns)

   if (att == in_att) :
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
            if dfS[0] - dfS[1] != 0 and  dfS[1] - dfS[2] != 0:   #find ambigious
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
      global ambilist 
      ambilist = ambi.to_json(orient="values")
      print(ambilist)

      #write csv
      sus.to_csv('suspect.csv', index=False)
      ambi.to_csv('ambigious.csv', index=False)

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

      bad_review = {
         'Name' : name,
         'Assignment' : asn,
         'Bad Reviewer' : bname,
         'Score' : bscore
      }

      bad = pd.DataFrame(bad_review)

      # list of bad reviewers to display in the table. 
      global badlist
      badlist = bad.to_json(orient="values")

      bad.to_csv('bad_reviewer.csv', index=False)

      return jsonify("processing")
   else :
      return jsonify("process-error")


@app.route('/processing-error')
def ProcessError():
   return render_template("processError.html")

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