# from flask import Flask,render_template

import os
from flask import Flask,request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	
@app.route('/')
def Home():
   return render_template("upload.html")

@app.route('/upload-error')
def UploadError():
   return render_template("uploadError.html")

@app.route('/processing')
def Processing():
   return render_template("process.html")

@app.route('/process-error')
def ProcessError():
   return render_template("processError.html")

@app.route('/result')
def Result():
   return render_template("result.html")

def allowed_file(filename):
   return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
      f = request.files['filename']
      #   file = secure_filename(f.filename)
      #   f.save(os.path.join (app.config['UPLOAD_FOLDER'],file))
      if f and allowed_file(f.filename) :
         # filename = secure_filename(f.filename)
         f.save(os.path.join (app.config['UPLOAD_FOLDER'],f.filename))
         return redirect(url_for('Processing'))
      else :
         return render_template("uploadError.html")

if __name__ == '__main__':
 app.debug = True
 app.run(host='0.0.0.0', port=8000)