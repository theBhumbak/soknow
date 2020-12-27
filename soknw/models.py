from datetime import datetime
from flask_login import UserMixin
from soknw import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

reads = db.Table('reads',
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id',db.Integer, db.ForeignKey('book.id'), primary_key=True))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avtar =  db.Column(db.String(20), nullable=False, default='defaultavtar.jpg')
    password= db.Column(db.String(60), nullable=False)
    readin = db.relationship('Book', secondary=reads, backref=db.backref('reader', lazy = 'dynamic') )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avtar}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(20), nullable=False, default=f'static/images/Bookcovers/defaulcover.jpg')
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    discription = db.Column(db.Text, nullable=True)
    # reader = db.relationship("User", secondary='Reads', backref=db.backref('reader', lazy = 'dynamic'))

    def __repr__(self):
        return f"User('{self.title}', '{self.author}')"