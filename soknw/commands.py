import click
from flask.click import with_appcontext

from soknw import db
from .models import Book, User

@click.command(name='create_table')
@with_appcontext
def create_table():
    db.create_all