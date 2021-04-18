from flask import Flask
from flask import render_template
from newsapi import NewsApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def Index():
    newsapi = NewsApiClient(api_key="87a33682f0fc4efa9f36e2336b721304")
    topheadlines = newsapi.get_top_headlines(sources="cnn")
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []

    for new in articles:
        print(new)
        news.append(new['title'])
        desc.append(new['description'])
        img.append(new['urlToImage'])
        url.append(new['url'])
    mylist = zip(news, desc, img, url)
    return render_template('index.html', context=mylist)


if __name__ == "__main__":
    app.run(debug=True)