"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
Alan = User(first_name='Alan', last_name="Alda", image_url="https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA17aUdT.img?w=768&h=512&m=6&x=73&y=13&s=943&d=430")
Joel = User(first_name='Joel', last_name="Burton")
Jane = User(first_name='Jane', last_name="Smith")

# Add new objects to session, so they'll persist
db.session.add(Alan)
db.session.add(Joel)
db.session.add(Jane)

# Commit--otherwise, this never gets saved!
db.session.commit()
