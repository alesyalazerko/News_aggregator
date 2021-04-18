from datetime import datetime
from app import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(400), nullable=False, unique=True)
    urlToImage = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    '''def __init__(self, id, title, description, urlToImage, url):
        self.id = id
        self.title = title
        self.description = description
        self.urlToImage = urlToImage
        self.url = url'''

    def __repr__(self):
        return f'<New {self.title}>'
