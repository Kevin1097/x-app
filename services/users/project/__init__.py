# services/users/project/__init__.py


import os  # nuevo

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

# instanciado la app
db = SQLAlchemy()  # nuevo
toolbar = DebugToolbarExtension()
cors = CORS()


def create_app(script_info=None):
    # instanciado la app
    app = Flask(__name__)


# establecer configuraicon
    app_settings = os.getenv('APP_SETTINGS')   # Nuevo
    app.config.from_object(app_settings)       # Nuevo

# cofiguramos la extension
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)

# registramos los blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
