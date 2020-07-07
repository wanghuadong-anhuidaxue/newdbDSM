from flask import Flask
from App.ext import init_ext
from App.views import init_view
from App.setting import envs


def create_app(env):
    app = Flask(__name__, static_url_path='/newdbDSM', static_folder='static')
    app.config.from_object(envs.get(env))
    # app.config.update()
    init_ext(app=app)
    init_view(app=app)
    return app

