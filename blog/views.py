import re
import datetime
from blog import app
from blog.database import create_entry, check_users, retrieve_entries, retrieve_entry, replace_content_entry
from flask import Blueprint, render_template, request, session
from functools import wraps
from bs4 import BeautifulSoup

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
    entries = retrieve_entries()
    entry_titles = []

    blog_to_display = retrieve_entry(request.args.get('article_id'))

    if blog_to_display == None:
        return render_template("blog.html",entries=entries, entry=entries[-1] )

    return render_template("blog.html",entries=entries, entry=blog_to_display ) 

def cleanhtml(raw_html):
    # cleanr = re.compile('<.*?>') 
    # cleantext = re.sub(cleanr, '', raw_html)
    # return cleantext
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()

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
    entries = retrieve_entries()

    blog_to_edit = retrieve_entry(request.args.get('article_id'))

    if request.method == "POST":
        if "add" in request.form:
            entry_content = request.form.get('editordata')
            create_entry(datetime.datetime.today().strftime("%Y %b %d"), cleanhtml(entry_content[0:30]), entry_content)

            return render_template("blogcreate.html", entries=retrieve_entries(), entry=blog_to_edit)

        if "edit" in request.form:
            entry_content = request.form.get('editordata')
            replace_content_entry(request.args.get('article_id'), cleanhtml(entry_content[0:30]), entry_content)
            return render_template("blogcreate.html", entries=retrieve_entries(), entry=blog_to_edit)
    else:
        return render_template("blogcreate.html", entries=retrieve_entries(), entry=blog_to_edit)
