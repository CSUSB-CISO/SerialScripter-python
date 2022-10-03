from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# This is a one to many relationship between user and key
# meaning only the user who created the note has access to modify or delete
# there is a such thing as many to one relationship which I have not looked into

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # type of column is integer and foreign key means that we must pass a valid id of existing user to that column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
#Parent
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    keys = db.relationship('Key')