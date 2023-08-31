from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/files')
def files():
    return render_template('files.html')

@views.route('/upload')
def upload():
    return render_template('upload.html')