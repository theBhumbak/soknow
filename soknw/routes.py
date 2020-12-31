import os
import string 
import random 
import bcrypt
from PIL import Image
from flask_admin import AdminIndexView
from soknw import app, db, admin
from soknw.models import Book, User
from soknw.forms import (LoginForm, 
                        RegistrationForm,
                        UpdateAccountForm)
from flask_login import (current_user,
                        login_required,
                        login_user, logout_user)
from flask import (Flask, flash, redirect,
                    render_template, request, 
                    url_for, send_file, 
                    send_from_directory, abort)
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

app.config['allbooks']= os.path.join(os.path.dirname(__file__), 'static/books/PDFs')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title='Home')

@app.route('/library')
def library():
    books = Book.query.all()
    return render_template('library.html', books=books, coverdic = "static/Bcov/", title='Library')

@app.route("/library/<int:book_id>/")
def book(book_id):
    book = Book.query.get(book_id)
    book_title = book.title
    book_id = book_id
    return render_template('book.html', title='book', book_title =book_title, book_id = book_id)

@app.route("/library/get/<int:book_id>/")
def getbook(book_id):
    bookname = Book.query.get(book_id).title + ".pdf"

    try:
        return send_from_directory(
            app.config["allbooks"], filename=bookname, as_attachment=False
            )
    except FileNotFoundError:
        abort(404)

# -------Admin Views------

class MyModelView(ModelView):
    def is_accessible(self):
        print(f"current_user.is_authenticated : {current_user.is_authenticated} ; and current_user.id : {current_user.get_id()}; in os.environ(ADMINLS): {os.environ['ADMINLS']};")
        return (current_user.is_authenticated 
        and current_user.get_id() in os.environ['ADMINLS'])

    def inaccessible_callback(self, name, **kwargs):
        return "<h1>Only Admins Allowed</h1>"

class MyAdminIndexView (AdminIndexView):
    def is_accessible(self):
        print(f"current_user.is_authenticated : {current_user.is_authenticated} ; and current_user.id : {current_user.get_id()}; in os.environ(ADMINLS): {os.environ['ADMINLS']};")
        return (current_user.is_authenticated 
        and current_user.get_id() in os.environ['ADMINLS'])

    def inaccessible_callback(self, name, **kwargs):
        return "<h1>Only Admins Allowed</h1>"

# ---- path to ststic folder
staticfilepath = os.path.join(os.path.dirname(__file__), 'static')

# admin.init_app(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Book, db.session))

admin.add_view(FileAdmin(staticfilepath, '/static/', name='Static Files'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        hashed = bcrypt.hashpw(form.password.data.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        print('check 4: password hashed sucessfull')
        user = User(username=form.username.data,name=form.name.data,email=form.email.data,password=hashed)
        db.session.add(user)
        db.session.commit()
        print('pasword saved sucessfully')
        flash(f'Account created for {form.username.data}!', 'green accent-1')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('password', bcrypt.checkpw(form.password.data.encode('utf8'), user.password.encode()))
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'red accent-1' )
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form =UpdateAccountForm()
    if form.validate_on_submit():
        if form.avtar.data:
            avtar_file = save_avtar(form.avtar.data)
            current_user.avtar = avtar_file
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'green accent-1')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    avtar = url_for('static', filename = f'images/Profile_pictures/{ current_user.avtar }')
    # { current_user.avtar }
    return render_template('account.html', title='Account', avtar=avtar, form=form)

def save_avtar(avtar):

    # createing random string for name of  picture

    # initializing size of string  
    N = 8
    random_hex = ''.join(random.choices(string.ascii_uppercase + 
            string.digits, k = N))
    

    # extracting file name and file extention    
    _, f_ext = os.path.splitext(avtar.filename)
    image_flnm = random_hex + f_ext # new name for file
    large_image_flnm = random_hex + '-large' + f_ext
    
    # absolute path to save the file
    image_path = os.path.join(app.root_path, 'static/images/Profile_pictures',image_flnm)
    large_image_path = os.path.join(app.root_path, 'static/images/Profile_pictures',large_image_flnm)
    # RESIZING
    output_size = (125,125)
    i= Image.open(avtar)
    i.thumbnail(output_size)
    i.save(image_path) # SAVING THE smaller FILE IN FOLDER
    avtar.save(large_image_path) # SAVING THE original FILE IN FOLDER
    return image_flnm #RETURNING NAME OF FILE TO UPDATE IN DATABASE

# routefor favicon
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')
