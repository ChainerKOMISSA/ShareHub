from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('views.files', user_id = user_id))
        else:
            flash('Identifiants incorrects, Veuillez réessayer', category='error')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return redirect(url_for('views.home'))