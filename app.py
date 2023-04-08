from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import *
import sqlite3
import json

# --------------------------------------------------------------------------------------

app = Flask(_name_, template_folder='templates')
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_show.db'
app.config['TESTING'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


# Login Manager-------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    # return the user object for the user with the given user_id
    return Users.query.get(int(user_id))


isAdmin = False

# Models--------------------------------------------------------------------------------

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)
    usr_name = db.Column(db.String(30), nullable = False)
    username = db.Column(db.String(30), nullable = False)
    usr_phone = db.Column(db.Integer(), nullable = False)
    usr_mail = db.Column(db.String(40), nullable = False)
    roles = db.Column(db.String(20), default = 'user')

    def get_id(self):
           return (self.user_id)

    def _repr_(self):
        return "<User %r>" % self.user_id

    def isAdmin(self): 
        if self.roles == 'admin':
            return True
        else:
            return False
            
class Venues(db.Model):
    venue_id = db.Column(db.Integer(), primary_key = True)
    venue_name = db.Column(db.String(50), nullable = False)
    venue_place = db.Column(db.String(50), nullable = False)
    venue_location = db.Column(db.String(50), nullable = False)
    venue_capacity = db.Column(db.Integer(), nullable = False)
    shows = db.relationship("Shows", back_populates="venues", cascade="all, delete")

    def _repr_(self):
        return "<Venue %r>" % self.venue_id


class Shows(db.Model):
    show_id = db.Column(db.Integer(), primary_key = True)
    show_name = db.Column(db.String(50), nullable = False)
    show_time = db.Column(db.String(50), nullable = False)
    show_tag = db.Column(db.String(50), nullable = False)
    show_rating = db.Column(db.Integer(), nullable = False)
    show_price = db.Column(db.Integer(), nullable = False)
    svenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id', ondelete='CASCADE'))
    venues = db.relationship("Venues", back_populates="shows")
    def _repr_(self):
        return "<Shows %r>" % self.show_id
            
            

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
