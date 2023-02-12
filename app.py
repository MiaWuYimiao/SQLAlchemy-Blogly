"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from sqlalchemy.sql import text
from models import db, connect_db, User, Post
from datetime import datetime

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
    """Homepage show recent blogly posts"""

    posts = Post.query.order_by(Post.create_at).limit(5).all()
    return render_template("home.html", posts = posts)

@app.route("/users")
def list_Users():
    """List users and show add button"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users = users)


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
    
    flash(f"User {user.full_name} added.")

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_detail_page(user_id):
    """Show detail information of the user"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user, posts=user.posts)

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

    flash(f"User {user.full_name} edited")

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to users page"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.full_name} deleted")
    return redirect("/users")


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_add_post_page(user_id):
    """Show page with form to add a new post to that user"""

    user = User.query.get_or_404(user_id)
    return render_template("postForm.html", user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle add form and add post and redirect to the user detail page"""

    title = request.form.get("title")
    content = request.form.get("content")

    post = Post(title=title, content=content, create_at=datetime.now(), user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' added")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post = post)


@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_post_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""

    post = Post.query.get_or_404(post_id)
    return render_template("postEdit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited")

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' deleted")

    return redirect(f"/users/{user_id}")

@app.errorhandler(404)
def not_found(e):
    """Redirect to 404 error page"""

    return render_template("404.html")