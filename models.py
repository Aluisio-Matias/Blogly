"""Models for Blogly."""
from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/computer-user-icon-8.png"




class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        '''Shows the user's full name'''
        s = self
        return f'{s.first_name} {s.last_name}'


def connect_db(app):
    db.app = app
    db.init_app(app)