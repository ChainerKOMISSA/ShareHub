from flask import Blueprint, render_template, request, flash
from .models import user
from . import db



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        utilisateur = user.query.filter_by(emailuser=email).first()
        if utilisateur:
            if user.passworduser == password:
                flash('Connexion réussie!', category='success')
            else:
                flash('Mot de passe incorrect, Veuillez réessayer', category='error')
        else:
            flash('Email incorrect, Veuillez réessayer', category='error')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "Logout"