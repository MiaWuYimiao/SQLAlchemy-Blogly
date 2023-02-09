"""Blogly application."""

from flask import Flask, request, redirect, render_template
from sqlalchemy.sql import text
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)
db.create_all()


from flask_debugtoolbar import  DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET"
debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    """Homepage redirects to list of users"""

    return redirect('/users')

@app.route("/users")
def list_Users():
    """List users and show add button"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("home.html", users = users)


@app.route('/users/new')
def go_to_form():
    """Go to User Form page"""
    return render_template("form.html")

@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Add new user and redirect to users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']

    user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_detail_page(user_id):
    """Show detail information of the user"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """Show page to edit existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edit the user information and redirect to users page"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get('first_name', user.first_name)
    user.last_name = request.form.get('last_name', user.last_name)
    user.image_url = request.form.get('url', user.image_url)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user and redirect to users page"""
    
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")

