from flask import Flask
from App.ext import init_ext
from App.views import init_view
from App.setting import envs
from pathlib import Path

def create_app(env):
    app = Flask(__name__, static_url_path='/newdbDSM', static_folder='static')
    app.config.from_object(envs.get(env))

    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 将网站允许的最大文件设置为5MB，防止拖垮网站
    app.config['UPLOAD_PATH'] = Path(app.root_path).joinpath('files/uploads')  # 设置网站上传文件的路径
    app.config['RESULT_PATH'] = Path(app.root_path).joinpath('files/pred_result')  # 设置预测结果路径
    Path(app.config['UPLOAD_PATH']).mkdir(exist_ok=True, parents=True)  # 避免因目录不存在而报错
    Path(app.config['RESULT_PATH']).mkdir(exist_ok=True, parents=True)


    init_ext(app=app)
    init_view(app=app)
    return app

