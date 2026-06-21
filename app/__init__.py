from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dss_ahp_topsis_secret_key'
    
    # Configure SQLite Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'dss.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.smartphone_routes import smartphone_bp
    from app.routes.dss_routes import dss_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(smartphone_bp, url_prefix='/smartphones')
    app.register_blueprint(dss_bp, url_prefix='/dss')

    return app
