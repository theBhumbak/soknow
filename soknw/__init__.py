from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin



# TODOS
#     -1. visual feedback of form validation

app = Flask(__name__)
app.config['SECRET_KEY']='d2d97cb8f25a23d315d1174d054f27e6'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'red-text text-accent-1'
admin = Admin()
# import routes from sonkw here(below everything else) to avoid complications of circular importing
from soknw import routes
admin.init_app(app, index_view=routes.MyAdminIndexView())
