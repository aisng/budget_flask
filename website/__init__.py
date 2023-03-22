from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin


basedir = path.abspath(path.dirname(__file__))
DB_NAME = "database.sqlite"

admin = Admin()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "42c2deb226a6ebe6483aface7c42448c"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(basedir, DB_NAME)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)

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
    if not path.exists(basedir + DB_NAME):
        db.create_all()
