import re
from blog.database import create_entry, check_users, retrieve_entries
from blog import app
from flask import Blueprint, render_template, request, session
from functools import wraps

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html")

@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_candidate = request.form['password'] 

        if check_users(username,password_candidate):
            session['logged_in'] = True

    return render_template("login.html")

@app.route("/blog", methods=["GET"])
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

@app.route("/blogcreate", methods=["GET", "POST"])
@is_logged_in
def blogcreate():   
    if request.method == "POST":
        entry_content = request.form.get('editordata')
        create_entry(entry_content, datetime.datetime.today().strftime("%b %d"))

        return render_template("blogcreate.html", entries=retrieve_entries())
    else:
        return render_template("blogcreate.html")