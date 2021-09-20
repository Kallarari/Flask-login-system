import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from flask import send_from_directory


app = Flask(__name__)

#é preciso um app e um DataBase antes das rotas, por isso importo depois
from app.controllers import routes