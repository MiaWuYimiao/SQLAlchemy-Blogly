"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cvhrma.org/wp-content/uploads/2015/07/default-profile-photo.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                            nullable=False)
    last_name = db.Column(db.String(50),
                            nullable=False)
    image_url = db.Column(db.VARCHAR(),
                            nullable=True,
                            default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post',
                            backref="user",
                            cascade="all, delete-orphan")


    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"

    def get_full_name(self):
        """Return full name"""

        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        """Return full name"""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    create_at = db.Column(db.DateTime,
                            nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    @property
    def friendly_date(self):
        """Get user read friendly date time"""

        return self.create_at.strftime("%a %b %-d  %Y, %-I:%M %p")



