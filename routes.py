import os
from newsapi import NewsApiClient
from datetime import datetime
from models import *
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, login, db
from forms import LoginForm, RegistrationForm
from models import User


@login.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.rememberMe.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(),
                    email=form.email.data.lower(),
                    phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/get_news')
def get_news_list():
    newsapi = NewsApiClient(api_key=os.environ.get('API_KEY'))
    topheadlines = newsapi.get_top_headlines(sources="the-verge,bbc-news,cnn, fox-news,"
                                                     " politico, abc-news, usa-today, ")
    articles = topheadlines['articles']

    for article in articles:
        new = News()
        print(article['publishedAt'].replace('T', ' ')[:16])
        try:
            new.title = article['title']
            new.source = article['source']['name']
            new.description = article['description']
            new.urlToImage = article['urlToImage']
            new.url = article['url']
            new.created_at = datetime.strptime(article['publishedAt'].replace('T', ' ')[:16], '%Y-%m-%d %H:%M')

            db.session.add(new)
            db.session.commit()
        except:
            print(article['title'])

    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    news = News.query.order_by(News.created_at.desc()).all()
    return render_template('index.html', news=news)