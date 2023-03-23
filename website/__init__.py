from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_mail import Mail
from config import Config


admin = Admin()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Entry
    from .admin_view import AdminModelView

    create_database()

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Entry, db.session))

    return app


def create_database():
    if not path.exists(Config.SQLALCHEMY_DATABASE_URI):
        db.create_all()
