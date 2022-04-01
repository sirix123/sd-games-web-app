from flask import Blueprint, render_template, Flask
from blog import db
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256),  nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(50000), nullable=False)

    def __repr__(self):
        return '<title %r>' % self.title

def create_entry(date, title, content):
    entry = Article(date=date, title=title, content=content )
    db.session.add(entry)
    db.session.commit()
    # print(Article.query.all())

def replace_content_entry(article_id_get, title, content):
    article = Article.query.filter_by(article_id = article_id_get).first()
    article.title = title
    article.content = content
    db.session.commit()

def retrieve_entries():
    return Article.query.all()

def retrieve_entry(article_id_get):
    article = Article.query.filter_by(article_id = article_id_get).first()
    if article == None:
        return None
    else:
        return article

def check_users(username,password_candidate):
    
    admin_login = User.query.filter_by(username = username).all()
    for user in admin_login:
        if( sha256_crypt.verify(password_candidate, user.password) ):
            # print("logged in")
            return True
        else:
            print("no username or password found")
