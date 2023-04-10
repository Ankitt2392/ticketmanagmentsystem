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
            
class Bookings(db.Model):
    booking_id = db.Column(db.Integer(), primary_key = True)
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete="CASCADE"))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    num_tickets = db.Column(db.Integer(), nullable = False)
    total_price = db.Column(db.Integer(), nullable = False)

    def _repr_(self):
        return "<Bookings %r%r%r>" % self.venue_id % self.show_id % self.booking_id


class Booked(db.Model):
    booked_id = db.Column(db.Integer(), primary_key = True)
    show_name = db.Column(db.String(50), primary_key = True, nullable = False)
    venue_name = db.Column(db.String(50), primary_key = True, nullable = False)
    seats_booked = db.Column(db.Integer(), default = 0)


class Ratings(db.Model):
    ratings_id = db.Column(db.String(20), primary_key = True)
    user_id = db.Column(db.Integer())
    show_name = db.Column(db.String(50), nullable = False)
    venue_name = db.Column(db.String(50), nullable = False)
    ratings = db.Column(db.Integer(), default = 0) 

 # Forms--------------------------------------------------------------------------------

class AdminLoginForm(FlaskForm):
    adminname = StringField('Admin Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UserRegisterationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordconf = PasswordField('Confirm Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    usermail = StringField('User Mail', validators=[DataRequired()])
    userphone = StringField('User Phone', validators=[DataRequired()])


class NewVenueForm(FlaskForm):
    venuename = StringField('Venue Name', validators=[DataRequired()])
    venueplace = StringField('Venue Place', validators=[DataRequired()])
    venueloc = StringField('Venue Location', validators=[DataRequired()])
    venuecap = StringField('Venue Capacity', validators=[DataRequired()])


class NewShowForm(FlaskForm):
    showname = StringField('Show Name', validators=[DataRequired()])
    ratings = StringField('Show Rating', validators=[DataRequired()])
    starttime = StringField('Show Time', validators=[DataRequired()])
    tags = StringField('Show Tag', validators=[DataRequired()])
    price = StringField('Show Price', validators=[DataRequired()])
    venue = StringField()


class NewTicketBookingForm(FlaskForm):
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    numseats = StringField('Number of Tickets', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])    
    total = StringField('Total Price', validators=[DataRequired()])

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
