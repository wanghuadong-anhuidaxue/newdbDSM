from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrade = Migrate()


def init_ext(app):
    db.init_app(app=app)
    migrade.init_app(app, db)
    bootstrap = Bootstrap(app)


