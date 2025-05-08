from flask import Flask
from .config import Config
from .extensions import db, migrate
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    # Desactiva el ordenamiento alfabético
    app.config['JSON_SORT_KEYS'] = False 

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    print(app.url_map)
    return app
