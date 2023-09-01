from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename, os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/files')
def files():
    return render_template('files.html')

@views.route('/upload')
def upload():
    '''if request.method == 'POST':
        nom = request.form['namefile']
        description = request.form['description']
        date = datetime.now()
        added = date.strftime('%d-%m-%Y %H:%M:%S')
        file = request.files['file']

        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        cursor = db.cursor()
        query = "INSERT INTO File (namefile, description, linkfile, added) " \
                "VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nom, description, image_path, added))
        db.commit()
        cursor.close()
        flash('Fichier déposé avec succès!', category='success')
        return redirect(url_for('views.files'))
    else :
        flash('Nous avons rencontré une erreur!', category='error')'''
    return render_template('upload.html')