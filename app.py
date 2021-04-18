from flask import Flask, render_template
from newsapi import NewsApiClient
'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
'''

app = Flask(__name__)
'''
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)




db.create_all()
'''


@app.route('/', methods=['GET', 'POST'])
def Index():

    newsapi = NewsApiClient(api_key="87a33682f0fc4efa9f36e2336b721304")
    topheadlines = newsapi.get_top_headlines(sources="cnn")


    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []


    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])



    mylist = zip(news, desc, img, url)


    return render_template('index.html', context = mylist)


if __name__ == "__main__":
    app.run(debug=True)