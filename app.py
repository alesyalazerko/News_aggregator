from flask import Flask, request, render_template
from newsapi import NewsApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from requests import request
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(400), nullable=False)
    urlToImage = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)

    '''def __init__(self, id, title, description, urlToImage, url):
        self.id = id
        self.title = title
        self.description = description
        self.urlToImage = urlToImage
        self.url = url'''

    def __repr__(self):
        return f'<New {self.title}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    newsapi = NewsApiClient(api_key="87a33682f0fc4efa9f36e2336b721304")
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
    mylist = []
    return render_template('index.html', context=mylist)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)