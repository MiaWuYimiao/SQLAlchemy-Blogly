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
