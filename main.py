# python main.py

from flask import Flask
from views import views
from database import database

app = Flask(__name__)
app.register_blueprint(views, url_prefix="")
app.register_blueprint(database, url_prefix="")
app.config['SECRET_KEY'] = 'adawdaw12312321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite'

if __name__ == "__main__":
    app.run(debug=True)