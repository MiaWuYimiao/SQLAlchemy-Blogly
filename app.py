"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from sqlalchemy.sql import text
from models import db, connect_db, User, Post, Tag, PostTag
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

    posts = Post.query.order_by(Post.create_at.desc()).limit(5).all()
    return render_template("home.html", posts = posts)

@app.route("/users")
def list_Users():
    """List users and show add button"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users = users)


@app.route('/users/new')
def go_to_form():
    """Go to User Form page"""
    return render_template("userForm.html")

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
    return render_template("userDetail.html", user=user, posts=user.posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """Show page to edit existing user"""

    user = User.query.get_or_404(user_id)
    return render_template("userEdit.html", user=user)

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
    tags = Tag.query.all()
    return render_template("postForm.html", user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle add form and add post and redirect to the user detail page"""

    title = request.form.get("title")
    content = request.form.get("content")

    tag_ids = [int(num) for num in request.form.getlist("taglist")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, create_at=datetime.now(), user_id=user_id,tags=tags)
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added")
    # taglist = request.form.getlist("taglist")
    # for tag_id in taglist:
    #     posttag = PostTag(post_id=new_post.id, tag_id=tag_id)
    #     db.session.add(posttag)
    #     db.session.commit()


    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the post"""

    post = Post.query.get_or_404(post_id)
    return render_template("postDetail.html", post = post)


@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_post_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("postEdit.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("taglist")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

@app.route('/tags')
def list_tags():
    """List all tags, with links to the tag detail page"""

    tags = Tag.query.all()

    return render_template("tags.html", tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete"""

    tag = Tag.query.get(tag_id)
    return render_template("tagDetail.html", tag=tag, posts=tag.posts)

@app.route('/tags/new', methods=["GET"])
def show_add_tag_page():
    """Shows a form to add a new tag"""

    posts = Post.query.all()
    return render_template("tagForm.html", posts=posts)

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Process add form, adds tag, and redirect to tag list."""

    post_ids = [int(num) for num in request.form.getlist("postlist")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()

    tagname = request.form["tagname"]
    newTag = Tag(name=tagname, posts=posts)

    db.session.add(newTag)
    db.session.commit()
    flash(f"Tag {tagname} added")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_form(tag_id):
    """Show edit form for a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("tagEdit.html", tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tagname"]

    post_ids = [int(num) for num in request.form.getlist("postlist")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag {tag.name} edited.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""
    
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag {tag.name} deleted.")

    return redirect('/tags')

@app.errorhandler(404)
def not_found(e):
    """Redirect to 404 error page"""

    return render_template("404.html")