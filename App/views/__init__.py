
from .homeblue import homeblue
from .submitblue import submitblue
from .searchblue import searchblue

from .testblue import testblue



def init_view(app):
    # app.register_blueprint(blue)
    app.register_blueprint(homeblue)
    app.register_blueprint(submitblue)
    app.register_blueprint(searchblue)
    app.register_blueprint(testblue)
