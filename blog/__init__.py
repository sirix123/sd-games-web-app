from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adawdaw12312321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite'
db = SQLAlchemy(app)

from blog import views
from blog import database

if __name__ == "__main__":
    app.run(debug=True)