
from .homeblue import homeblue
from .submitblue import submitblue
from .searchblue import searchblue
from .analysisblue import analysisblue
from .downblue import downblue



def init_view(app):
    app.register_blueprint(homeblue)
    app.register_blueprint(submitblue)
    app.register_blueprint(searchblue)
    app.register_blueprint(analysisblue)
    app.register_blueprint(downblue)
