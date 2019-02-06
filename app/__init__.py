from flask import Flask
from instance.config import app_config
from app.api.v1.politico import Politico

politico = Politico()

def create_app(config_name):
    app = Flask('__name__')
    app.config.from_object(app_config[config_name])

    from app.api.v1.blueprints import auth
    app.register_blueprint(auth.auth_blueprint)

    return app