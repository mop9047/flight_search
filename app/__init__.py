from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

def create_app():
    #Initialize the app from Flask
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

    app.secret_key = 'some key that you will never guess'
    
    #Configure MySQL
    app.config['db'] = pymysql.connect(host='localhost',
                        user='root',
                        password='root',
                        unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                        database='flights_new',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

