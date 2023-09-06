import os
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, send_file
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
            return redirect(url_for('files', user_id = user_id))
        else :
            flash('Nous avons rencontré une erreur!', category='error')
    return render_template('upload.html')

##READ

def get_icon_class(file_extension):
    icon_mapping = {
        'pdf': 'bi bi-file-earmark-pdf',
        'docx': 'bi bi-file-earmark-word',
        'txt': 'bi bi-filetype-txt',
        'xlsx': 'bi bi-file-earmark-excel',
        'png': 'bi bi-filetype-png',
        'jpg': 'bi bi-filetype-jpg',
        'jpeg': 'bi bi-filetype-jpg',
        'psd': 'bi bi-filetype-psd',
        'pub': 'bi bi-file-earmark-ppt',
        'pptx': 'bi bi-filetype-pptx',
        'zip':'bi bi-file-earmark-zip',
    }
    return icon_mapping.get(file_extension, 'bi-file')

def get_color_class(file_extension):
    color_mapping = {
        'pdf': '#FF2D00',
        'docx': '#2A60F3',
        'txt': '#313132',
        'xlsx': '#029506',
        'png': '#F913BC',
        'jpg': '#F913BC',
        'jpeg': '#F913BC',
        'psd': '#060694',
        'pub': '#03AB9B',
        'pptx': '#F05504',
        'zip': '#EABF00',
    }
    return color_mapping.get(file_extension, '#313132')


@app.route('/files/<string:user_id>', methods=['GET'])
def files(user_id):
    cursor = db.cursor()
    query = "SELECT * FROM File"
    cursor.execute(query)
    files = cursor.fetchall()
    cursor.close()

    files_formatted = []
    for file in files :
        linkfile = file[3]
        #print("##################")
        #print(linkfile)
        nom, extension = os.path.splitext(linkfile)
        color_class = get_color_class(extension[1:])

        format = {
            'id' : file[0],
            'namefile' : file[1],
            'description' : file[2],
            'linkfile': file[3],
            'extension': extension[1:],
            'added': file[4],
            'user_id' : file[5],
            'icon_class': get_icon_class(file[3].split('.')[-1]),
            'color_class' : color_class
        }
        files_formatted.append(format)
    return render_template('files.html', fichiers = files_formatted, user_id = user_id)

##UPDATE
@app.route('/edit/<string:user_id>/<int:file_id>', methods=['GET', 'POST'])
def edit_file(user_id, file_id):
    cursor1 = db.cursor()
    query = "SELECT * FROM File WHERE idfile = %s"
    cursor1.execute(query, (file_id,))
    file_data = cursor1.fetchone()
    cursor1.close()

    if file_data is None:
        flash('Fichier non trouvé!', category='error')
        return redirect(url_for('files', user_id=user_id))
    if request.method == 'POST':
        nom = request.form['namefile']
        description = request.form['description']
        date = datetime.now()
        added = date.strftime('%d-%m-%Y %H:%M:%S')
        fichier = request.files.get('fichier')

        filename = secure_filename(fichier.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fichier.save(image_path)

        cursor = db.cursor()
        query = "UPDATE File SET namefile = %s, description = %s, linkfile = %s, added = %s, user_id = %s WHERE idfile = %s"
        cursor.execute(query, (nom, description, image_path, added, user_id, file_id))
        db.commit()
        cursor.close()
        flash('Fichier modifié avec succès!', category='success')
        return redirect(url_for('files', user_id=user_id))
    return render_template('edit.html', file_data = file_data, user_id = user_id)




#DELETE
@app.route('/delete/<string:user_id>/<int:file_id>', methods=['POST'])
def delete(user_id, file_id):
    cursor = db.cursor()
    query = "DELETE FROM File WHERE idfile = %s"
    cursor.execute(query, (file_id,))
    db.commit()
    cursor.close()

    flash('Fichier supprimé', category='success')
    return redirect(url_for('files', user_id=user_id))

##TELECHARGEMENT DE FICHIER
@app.route('/download/<string:user_id>/<int:file_id>', methods=['GET'])
def download_file(user_id, file_id):
    cursor = db.cursor()
    query = "SELECT * FROM File WHERE idfile = %s"
    cursor.execute(query, (file_id,))
    file_data = cursor.fetchone()
    cursor.close()

    if file_data is None:
        flash('Fichier non trouvé!', category='error')
        return redirect(url_for('files', user_id=user_id))
    else :
        linkfile = file_data[3]
        if linkfile.startswith(app.config['UPLOAD_FOLDER']):
            return send_file(linkfile, as_attachment=True)
        else:
            flash('Fichier invalide', category='error')
            return redirect(url_for('files', user_id = user_id))


if __name__ == '__main__':
    app.run(debug=True)