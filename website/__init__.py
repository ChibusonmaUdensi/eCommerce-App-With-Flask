from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() 
DB_NAME = "database.db"

def create_database():
    db.create_all()
    print('Database created successfully')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mae'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))
   
    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order
    app.register_blueprint(views, url_prefix= '/') #localhost:5000/about-us
    app.register_blueprint(auth, url_prefix= '/') #localhost:5000/auth/change-password
    app.register_blueprint(admin, url_prefix= '/')


    # with app.app_context():
    #     create_database()

    return app