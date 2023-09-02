import os
from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_key'
upload_folder = r"static\fichiers"  # Dossier d'enregistrment des fichiers uploadées
app.config['UPLOAD_FOLDER'] = upload_folder

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shareandgodb",
)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = db.cursor()
        query = "SELECT * FROM User WHERE emailuser = %s AND passworduser = %s"
        cursor.execute(query, (email, password))
        utilisateur = cursor.fetchone()
        cursor.close()
        if utilisateur:
            user_id = utilisateur[0]
            flash('Connexion réussie!', category='success')
            return redirect(url_for('files', user_id = user_id))
        else:
            flash('Identifiants incorrects, Veuillez réessayer', category='error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('home.html')


##CREATE
@app.route('/upload/<string:user_id>', methods=['GET', 'POST'])
def upload(user_id):
    if request.method == 'POST':
        nom = request.form['namefile']
        description = request.form['description']
        date = datetime.now()
        added = date.strftime('%d-%m-%Y %H:%M:%S')
        fichier = request.files.get('fichier')

        if fichier is not None and fichier.filename != '':
            filename = secure_filename(fichier.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fichier.save(image_path)

            cursor = db.cursor()
            query = "INSERT INTO File (namefile, description, linkfile, added, user_id) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nom, description, image_path, added, user_id))
            db.commit()
            cursor.close()
            flash('Fichier déposé avec succès!', category='success')
            return render_template('files.html')
        else :
            flash('Nous avons rencontré une erreur!', category='error')
    return render_template('upload.html')

##READ
@app.route('/files/<string:user_id>', methods=['GET'])
def files(user_id):
    cursor = db.cursor()
    query = "SELECT * FROM File"
    cursor.execute(query)
    fichiers = cursor.fetchall()
    cursor.close()
    return render_template('files.html', fichiers = fichiers, user_id = user_id)



if __name__ == '__main__':
    app.run(debug=True)