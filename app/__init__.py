from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializa SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'tu_clave_secreta_unicaysecreta'
    
    # Inicializa la extensión de la base de datos con la aplicación
    db.init_app(app)
    
    # Inicializa Flask-Migrate
    migrate = Migrate(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    return app






