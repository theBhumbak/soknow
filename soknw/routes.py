import os
import secrets

import bcrypt
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from soknw import app, db
from soknw.forms import LoginForm, RegistrationForm, UpdateAccountForm
from soknw.models import Book, Library, User

books = [
        {
            'author':'Sumit Bhumbak',
            "image":" static\\images\\rashtravardhan.jpg ",
            "image_txt":" Kelly Sikkema ",
            'title':'Transforming India',
            'discription':'''in this book we look at the ways to make India the best country in the world''',
            'date_posted':'Feb 3rd, 2020'
        },
        {
            'author':'Sumit Bhumbak',
            "image":" static\\images\\thoughtcatalogGz.jpg ",
            "image_txt":"Morgan House",
            'title':'Changing The World',
            'discription':'''in this book we see how we are chinging thw world how can we further change this world for good''',
            'date_posted':'Feb 3rd, 2020'
        }
    ]
    
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        hashed = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt()).decode('utf-8')
        print('check 4')
        user = User(username=form.username.data,name=form.name.data,email=form.email.data,password=hashed)
        print('check 5')
        db.session.add(user)
        db.session.commit()
        print('check 6')
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
        print('password', bcrypt.checkpw(form.password.data.encode(), user.password.encode()))
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


@app.route('/library')
@login_required
def library():
    return render_template('library.html', books=books, title='Library')


def save_avtar(avtar):
    # createing random string for name of  picture
    random_hex = secrets.token_hex(8)
    print('---> random_hex is',random_hex)
    # ( _ ) => unused varible, dont bother your ide
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
