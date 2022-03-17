import re
from database import database, create_entry, check_users, retrieve_entries
from flask import Blueprint, render_template, request, session
from functools import wraps

views = Blueprint("views", __name__, static_folder = "static", template_folder = "templates")

@views.errorhandler(404)
def page_not_found(e):
    return render_template("index.html")

@views.route('/index')
@views.route('/')
def home():
    return render_template("index.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_candidate = request.form['password'] 

        if check_users(username,password_candidate):
            session['logged_in'] = True

    return render_template("login.html")

@views.route("/blog", methods=["GET"])
def blog():
    entry_titles = []
    entries = retrieve_entries()
    for i in entries:
        cleaned_title = cleanhtml(i[0][0:30])
        entry_titles.append(cleaned_title+" • "+i[1])

    print(entries[-1][0])
    return render_template("blog.html", entry_titles=entry_titles, entry_body=entries[-1][0] )

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return render_template("login.html")
    return wrap

@views.route("/blogcreate", methods=["GET", "POST"])
@is_logged_in
def blogcreate():   
    if request.method == "POST":
        entry_content = request.form.get('editordata')
        create_entry(entry_content, datetime.datetime.today().strftime("%b %d"))

        return render_template("blogcreate.html", entries=retrieve_entries())
    else:
        return render_template("blogcreate.html")