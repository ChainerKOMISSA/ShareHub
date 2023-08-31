from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
import mysql.connector

#db = SQLAlchemy()
#DB_NAME = "shareandgodb"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shareandgodb",
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_key'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #db.init_app(app)
    upload_folder = r"static\fichiers"  # Dossier d'enregistrment des fichiers uploadées
    app.config['UPLOAD_FOLDER'] = upload_folder

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app