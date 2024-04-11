from flask import Flask
import psycopg2
import psycopg2.extras

def get_db_connection():
    connection = psycopg2.connect(
        dbname='hyqsowhe',
        user='hyqsowhe',
        password='rSB75Si9GrLRGZVU_OHQYk4xY3lXG4Rw',
        host='isabelle.db.elephantsql.com'
    )
    connection.autocommit = True
    return connection

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta_unicaysecreta'
    
    from app import routes
    app.register_blueprint(routes.bp)

    return app




