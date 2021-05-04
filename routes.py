import os
from flask import render_template, redirect, url_for
from newsapi import NewsApiClient
from datetime import datetime
from app import app, db
from models import *

@app.route('/get_news')
def get_news_list():
    newsapi = NewsApiClient(api_key=os.environ.get('API_KEY'))
    topheadlines = newsapi.get_top_headlines(sources="cnn")
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
            pass

    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    news = News.query.order_by(News.created_at).all()
    return render_template('index.html', news=news)