import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "database.sqlite"


class Config:
    SECRET_KEY = os.environ.get("BUDGET_SECRET_KESY") or "verysecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
