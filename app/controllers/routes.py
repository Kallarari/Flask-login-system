import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from app.model.tabela import User
from app import app
from app.model.tabela import db

UPLOAD_FOLDER = 'app\static\img'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app.add_url_rule(
    "/static/img/<name>", endpoint="download_file", build_only=True
)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error="")
    if request.method == 'POST':
        nome = request.form['username']
        senha_user = request.form['password']
        compare = (User.query.filter_by(username=nome).first())
        if compare == None:
             return render_template('login.html', error="Usuário não encontrado!")
        if compare.senha == senha_user:
            return redirect(url_for('index', file_name=nome))
        else:
            return render_template('login.html', error="Senha incorreta!")
@app.route('/register.html', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
       nome = request.form['username']
       senha_user= request.form['password']
       novo_usuario = User(username=nome, senha=senha_user)
       db.session.add(novo_usuario)
       db.session.commit()
       return redirect('/')
    if request.method == 'GET':
        if user == None:
            return render_template('user_render.html', name=' não encontrado')
        return render_template('register.html')
@app.route('/index/<file_name>', methods=['GET', 'POST'])
def index(file_name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            usuario = (User.query.filter_by(username=file_name).first())
            return render_template('user_render.html', name=usuario.username, img=file_name)       
    if request.method == 'GET':
        return render_template('index.html', img='profile_blank.png', error='')