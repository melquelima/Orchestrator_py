from app import app,lm
from datetime import timedelta
import sys
from flask import send_from_directory,render_template,redirect,url_for,request,session
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
import os

@app.before_first_request
def initialize():
    print("Called only once, when the first request comes in")

@app.before_request
def before_request():
    session.permanent = True
    #app.permanent_session_lifetime = timedelta(seconds=5)

@app.route("/")
@login_required
def index():
    return render_template("main.html")

@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    #uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=app.root_path, filename=filename)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return {'ip': request.remote_addr,
            'ip2':request.environ['REMOTE_ADDR'],
            'ip3':request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            }, 200

@app.route("/curr")
def teste():
    return current_user

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if not request.files: return "No files found!"
    for file in request.files:
        file = request.files[file]
        if file.filename != '' and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Files uploaded!"

@app.route("/ip")
def ip():
    return request.headers["X-Forwarded-For"]