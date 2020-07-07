
from .homeblue import homeblue
from .submitblue import submitblue
from .searchblue import searchblue




def init_view(app):
    # app.register_blueprint(blue)
    app.register_blueprint(homeblue)
    app.register_blueprint(submitblue)
    app.register_blueprint(searchblue)
