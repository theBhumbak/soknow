from datetime import datetime

from flask_login import UserMixin

from soknw import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avtar =  db.Column(db.String(20), nullable=False, default='defaultavtar.jpg')
    password= db.Column(db.String(60), nullable=False)
    library = db.relationship('Library', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avtar}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(20), nullable=False, default=f'static/images/Bookcovers/defaulcover.jpg')
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    discription = db.Column(db.Text, nullable=True)
    library = db.relationship('Library', backref='book', lazy=True)

    def __repr__(self):
        return f"User('{self.title}', '{self.author}')"

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"User('{self.book}', '{self.mode}, {self.progress}')"
