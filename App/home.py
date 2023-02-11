# from flask import Flask,render_template

import os
from flask import Flask,request, render_template, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
# import pandas as pd
# from werkzeug.datastructures import  FileStorage


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fileName = ""
ambi = []
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
   # import time
   # time.sleep(200)
   df  = pd.read_csv("uploads/test2.csv")
   for i in range(0,len(df)):
    # เป็น ambigious
      if 1 >= abs((abs(df.iloc[i][3] - df.iloc[i][5])) - (abs(df.iloc[i][5] - df.iloc[i][7]))) :
         ambiatt = []
         for j in range(8) : 
            ambiatt.append(df.loc[i][j])
         ambi.append(ambiatt)
   return jsonify("oh so slow")


@app.route('/processing-error')
def ProcessError():
   return render_template("processError.html")

arrambi = [['A', 1, 'R', 9, 'T', 7, 'E', 5], ['B', 1, 'W', 7, 'U', 5, 'Y', 3], ['C', 1, 'E', 9, 'I', 7, 'S', 5], ['D', 1, 'W', 9, 'O', 8, 'H', 8]]
arrbad = [['A', 1, 'R', 9], ['A', 1, 'R', 9], ['A', 1, 'R', 9], ['A', 1, 'R', 9]]


@app.route('/result')
def Result():
   return render_template("result.html", ambiresult = arrambi, badresult = arrbad)

@app.route('/api/result')
def dowunloadFile():
   try:
	   return send_file('/var/www/PythonProgramming/PythonProgramming/static/images/python.jpg', attachment_filename='python.jpg')
   except FileNotFoundError:
        abort(404)



def allowed_file(filename):
   return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
      f = request.files['filename']
      if f and allowed_file(f.filename) :
         f.save(os.path.join (app.config['UPLOAD_FOLDER'],f.filename))
         fileName = f.filename
         return redirect(url_for('Processing'))
      else :
         return redirect(url_for('UploadError'))
    else: return redirect(url_for('UploadError'))

if __name__ == '__main__':
 app.debug = True
 app.run(host='0.0.0.0', port=8000)