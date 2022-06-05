from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import psycopg2
import psycopg2.extras

db = SQLAlchemy()
DB_HOST = "heffalump.db.elephantsql.com"
DB_NAME = "psakykxm"
DB_USER = "psakykxm"
DB_PASS = "kPekxJYmEC08AUYrNkil_emLpVNx5bCz"
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
def create_app():
    app = Flask(__name__)
    app.secret_key = 'dsfdsf sdfsad fdsf'
    app.config['SECRET_KEY'] = 'sjdfiosfjrerge erg'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://psakykxm:kPekxJYmEC08AUYrNkil_emLpVNx5bCz@heffalump.db.elephantsql.com/psakykxm'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Account

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Account.query.get(int(id))

    return app