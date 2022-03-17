from flask import Blueprint, render_template, Flask
from flask_sqlalchemy import SQLAlchemy

database = Blueprint("database", __name__, static_folder = "static", template_folder = "templates")
app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(5000), unique=True, nullable=False)

    def __repr__(self):
        return '<title %r>' % self.title

def create_entry(content, date):
    entry = Article(date=date, title='testtitle', content=content )
    db.session.add(entry)
    db.session.commit()
    print(Article.query.all())

# NEED TO REPLACE THE CONTENT OF THIS WITH ALCHELMY STUFF
def retrieve_entries():
    with sqlite3.connect("data.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RETRIEVE_ENTRIES)
        return cursor.fetchall()

# NEED TO REPLACE THE CONTENT OF THIS WITH ALCHELMY STUFF
def check_users(username,password_candidate):
    admin_login = User.query.filter_by(username=username).first()
    if admin_login:
        print("logged in")
    # with sqlite3.connect("data.db") as connection:
    #     cur = connection.cursor()
    #     cur.execute(("SELECT * FROM users WHERE username = ? AND password = ?"), (username,password_candidate))
    #     result = cur.fetchall()
    #     if result:
    #         return True
    #     else:
    #         print("no username or password found")

db.create_all()
# admin = User(username='sirix123', password='password123')
# db.session.add(admin)
# db.session.commit()
print(User.query.all())