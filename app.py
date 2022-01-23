"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'keep_it_a_secret'
app.debug = False
toolbar = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route('/')
def user_listing():
    '''Display list of all Users in db'''
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('/index.html', users=users)

@app.route('/new_user', methods=["GET"])
def new_user_form():
    '''Display the form to create a new user'''
    return render_template('/new_user.html')

@app.route('/new_user', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def show_user(user_id):
    '''Display specific users info'''
    user = User.query.get_or_404(user_id)
    return render_template('/show_user.html', user=user)

@app.route('/<int:user_id>/edit_user')
def edit_user(user_id):
    '''Display a form to edit an existing user'''
    user = User.query.get_or_404(user_id)
    return render_template('/edit_user.html', user=user)

@app.route('/<int:user_id>/edit_user', methods=["POST"])
def update_user(user_id):
    '''handle form for updating user'''

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''handle form submission to delete user'''

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')