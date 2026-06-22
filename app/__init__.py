from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dss_ahp_topsis_secret_key')
    app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'sura@dss.com')
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'SuraGG')
    
    # Configure SQLite Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'dss.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Authentication Middleware
    @app.before_request
    def check_login():
        # Allow access to static files, login/logout routes
        allowed_routes = ['auth.login', 'auth.logout', 'static']
        if request.endpoint not in allowed_routes and not session.get('logged_in'):
            return redirect(url_for('auth.login'))

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.smartphone_routes import smartphone_bp
    from app.routes.dss_routes import dss_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(smartphone_bp, url_prefix='/smartphones')
    app.register_blueprint(dss_bp, url_prefix='/dss')
    app.register_blueprint(auth_bp)

    return app
