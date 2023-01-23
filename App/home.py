from flask import Flask,render_template
app = Flask(__name__)
	
@app.route('/')
def Home():
   return render_template("upload.html")

@app.route('/processing')
def Processing():
   return render_template("process.html")

if __name__ == '__main__':
 app.debug = True
 app.run(host='0.0.0.0', port=8000)