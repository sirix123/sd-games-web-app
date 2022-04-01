from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite'
db = SQLAlchemy(app)

from blog import views
from blog import database

if __name__ == "__main__":
    app.run(debug=True)