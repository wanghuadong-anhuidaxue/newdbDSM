from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_bootstrap import Bootstrap
from flask_mail import Mail,Message

db = SQLAlchemy()
migrade = Migrate()
mail = Mail()

def init_ext(app):
    db.init_app(app=app)
    migrade.init_app(app, db)
    mail.init_app(app=app)
    # bootstrap = Bootstrap(app)


