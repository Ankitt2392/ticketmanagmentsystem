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

app = Flask(__name__, template_folder='templates')
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

    def __repr__(self):
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

    def __repr__(self):
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
    def __repr__(self):
        return "<Shows %r>" % self.show_id


class Bookings(db.Model):
    booking_id = db.Column(db.Integer(), primary_key = True)
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id', ondelete="CASCADE"))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    num_tickets = db.Column(db.Integer(), nullable = False)
    total_price = db.Column(db.Integer(), nullable = False)

    def __repr__(self):
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


class UpdateShowForm(FlaskForm):
    showname = StringField('Show Name', validators=[DataRequired()])
    ratings = StringField('Show Rating', validators=[DataRequired()])
    starttime = StringField('Show Time', validators=[DataRequired()])
    tags = StringField('Show Tag', validators=[DataRequired()])
    price = StringField('Show Price', validators=[DataRequired()])
    showid = StringField()


class UpdateVenueForm(FlaskForm):
    venuename = StringField('Venue Name', validators=[DataRequired()])
    venueplace = StringField('Venue Place', validators=[DataRequired()])
    venueloc = StringField('Venue Location', validators=[DataRequired()])
    venuecap = StringField('Venue Capacity', validators=[DataRequired()])
    venueid = StringField()


class DataForm(FlaskForm):
    booking_show = StringField()
    booking_venue = StringField()
    search_items = StringField()


class UserUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    usermail = StringField('User Mail', validators=[DataRequired()])
    userphone = StringField('Phone Number', validators=[DataRequired()])
    existingpassword = StringField('Existing Password', validators=[DataRequired()])
    newuserpassword = StringField('New Password')
    confuserpassword = StringField('Confirm New Password')


class RatingForm(FlaskForm):
    venue = StringField()
    show = StringField()
    rating = StringField()

# Admin creation -----------------------------------------------------------------------------

# if not (Users.query.filter_by(roles='admin').first()):
# print("New Admin created")
# user = Users(password=generate_password_hash("admin123"), usr_name="admin", usr_phone=9876543210, usr_mail="admin@gmail.com", username="Admin")
# db.session.add(user)
# db.session.commit()
# login_user(user)

# Routes-------------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("welcome.html", title="Welcome Page")


@app.route('/adminlogin', methods =["GET", "POST"])
def adminlogin():
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(usr_name=form.adminname.data).first()
        if user and Users.isAdmin(user):
            if user.password == form.password.data:
                isAdmin = True
                login_user(user)
                return redirect(url_for('admindashboard'))
            else:
                flash('Invalid credentials!!')
                return redirect(url_for('adminlogin'))
        else:
            flash('Invalid User!!')
    return render_template('admin_login.html', title='Admin Login', form=form)


@app.route('/login', methods =["GET", "POST"])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(usr_name=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login Successful!!")
                return redirect(url_for('userdashboard'))
            else:
                flash('Invalid credentials!!')
                return redirect(url_for('login'))
        else:
            flash('User not found!!')
    return render_template('user_login.html', title='User Login', form=form)


@app.route('/registeration', methods =["GET", "POST"])
def user_registeration():
    form = UserRegisterationForm()

    if form.validate_on_submit():
        if form.password.data == form.passwordconf.data:
            hashed_password = generate_password_hash(form.password.data)
            user = Users(password=hashed_password, usr_name=form.username.data, usr_phone=form.userphone.data, usr_mail=form.usermail.data, username=form.name.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Registeratin Successful!!")
            return redirect(url_for('login'))
        else:
            flash("Passwords do not match!!")
            return redirect(url_for('user_registeration'))
    return render_template('registeration.html', title='User Registeration', form=form)


@app.route('/userdashboard', methods =["GET", "POST"])
@login_required
def userdashboard():
    form = DataForm()
    pkey = 0
    searchkey = ''
    form_content = request.form.to_dict()

    if request.method == 'POST' and len(form_content)==1:
        pkey=1
        searchkey = request.form['searchitem']
        print(searchkey)
        fvenuelist = []
        svenplace = Venues.query.filter(Venues.venue_place.ilike(searchkey+'%')).all()
        svenloc = Venues.query.filter(Venues.venue_location.ilike(searchkey+'%')).all()
        svenname = Venues.query.filter(Venues.venue_name.ilike(searchkey+'%')).all()
        sshotag = Shows.query.filter(Shows.show_tag.ilike(searchkey+'%')).all()
        sshoname = Shows.query.filter(Shows.show_name.ilike(searchkey+'%')).all()

        # To check for place related shows
        if svenplace :
            venplace=[]
            sven = Venues.query.filter(Venues.venue_place.ilike(searchkey+'%')).all()
            for ven in sven:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                venplace.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = venplace

        # To check for location related shows
        elif svenloc :
            venloc=[]
            sven = Venues.query.filter(Venues.venue_location.ilike(searchkey+'%')).all()
            for ven in sven:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                venloc.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = venloc

        # To check for venue names related shows
        elif svenname :
            venname=[]
            sven = Venues.query.filter(Venues.venue_name.ilike(searchkey+'%')).all()
            for ven in sven:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                venname.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = venname

        # To check for tags related shows
        elif sshotag :
            shotag=[]
            ssho = Shows.query.filter(Shows.show_tag.ilike(searchkey+'%')).all()
            sven=[]
            for sho in ssho:
                veid = Venues.query.filter(Venues.venue_id==sho.svenue_id).first()
                sven.append(veid)
            for ven in sven:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                shotag.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = shotag

        # To check for show name related shows
        elif sshoname :
            shoname=[]
            ssho = Shows.query.filter(Shows.show_name.ilike(searchkey+'%')).all()
            sven=[]
            for sho in ssho:
                veid = Venues.query.filter(Venues.venue_id==sho.svenue_id).first()
            sven.append(veid)
            for ven in sven:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                shoname.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = shoname

        else :
            venues = Venues.query.all()
            venu=[]
            for ven in venues:
                shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
                show=[]
                for sho in shows:
                    show.append({"name": sho.show_name, "time": sho.show_time})
                venu.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
            fvenuelist = venu

    if pkey == 0:
        venues = Venues.query.all()
        venu=[]
        for ven in venues:
            shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
            show=[]
            for sho in shows:
                show.append({"name": sho.show_name, "time": sho.show_time})
            venu.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity})
        fvenuelist = venu

    if form.validate_on_submit():
        session['venue_name'] = form.booking_venue.data
        session['show_name'] = form.booking_show.data
        return redirect(url_for('ticketbooking'))

    return render_template('user_dashboard.html', title='User Dashboard', form=form, data=fvenuelist)


@app.route('/admindashboard', methods =["GET", "POST"])
@login_required
def admindashboard():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    venues = Venues.query.all()
    venu=[]
    for ven in venues:
        shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
        show=[]
        for sho in shows:
            show.append({"name": sho.show_name, "time": sho.show_time, "showid": sho.show_id, "tag": sho.show_tag, "price": sho.show_price, "rating": sho.show_rating})
        venu.append({"name": ven.venue_name, "cards": show, "place": ven.venue_place, "location": ven.venue_location, "capacity": ven.venue_capacity, "venueid": ven.venue_id})
    return render_template('admin_dashboard.html', title='Admin Dashboard', data=venu)


@app.route('/profile', methods =["GET", "POST"])
@login_required
def profile():
    usrdet = Users.query.filter_by(user_id=current_user.user_id).first()
    details = {"usr_name":usrdet.usr_name, "usr_phone":usrdet.usr_phone, "usr_mail":usrdet.usr_mail, "username":usrdet.username, "password":usrdet.password}
    
    form = UserUpdateForm()
    if form.validate_on_submit():
        if check_password_hash(usrdet.password, form.existingpassword.data):
            if form.newuserpassword.data == form.confuserpassword.data:
                hashed_password = generate_password_hash(form.newuserpassword.data)
                user = Users(password=hashed_password, usr_name=form.username.data, usr_phone=form.userphone.data, usr_mail=form.usermail.data, username=form.name.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash("Successfully Changed Data!!")
                return redirect(url_for('userdashboard'))
            else:
                flash("Enter the same password!!")
                return redirect(url_for('profile'))
        else:
            flash("Enter the correct password!!")
            return redirect(url_for('profile'))

    return render_template('profile.html', title='Profile', form=form, data=details)


@app.route('/ticketbooking', methods =["GET", "POST"])
@login_required
def ticketbooking():
    try:
        form = NewTicketBookingForm()
        booking_venue = session['venue_name']
        booking_show = session['show_name']

        if form.validate_on_submit():
            show_id = (Shows.query.filter_by(show_name = booking_show).first_or_404()).show_id
            venue_id = (Venues.query.filter_by(venue_name = booking_venue).first_or_404()).venue_id
            booking = Bookings(num_tickets=form.numseats.data, bvenue_id=venue_id, bshow_id=show_id, total_price=form.total.data, buser_id=current_user.user_id)
            db.session.add(booking)
            
            #Variable to keep track of number of bookings
            booked_count = len(Booked.query.all())+1
            booked = Booked(show_name=booking_show, venue_name=booking_venue, seats_booked=form.numseats.data, booked_id=booked_count)
            db.session.add(booked)
            
            db.session.commit()
            flash("Booking confirmed!!")
            return redirect(url_for('userdashboard'))
        
        show_time = (Shows.query.filter_by(show_name = booking_show).first_or_404()).show_time
        total_seats = (Venues.query.filter_by(venue_name = booking_venue).first_or_404()).venue_capacity
        show_price = (Shows.query.filter_by(show_name = booking_show).first_or_404()).show_price


        booked_seats = Booked.query.filter_by(show_name = booking_show).first()
        if (booked_seats == None):
            booked_seats = 0
        else:
            booked_seats = booked_seats.seats_booked
        available_seats = total_seats - booked_seats

        booking_detail = {'booking_venue':booking_venue, 'booking_show':booking_show, 'show_time':show_time, 'total_seats':total_seats, 'available_seats':available_seats, 'price':show_price}
        return render_template('ticket_book.html', title='Ticket Booking', form=form, booking_detail=booking_detail)
    except Exception as e:
        # For Debugging purposes
        print(e)
        flash('Something went wrong!!')
        return redirect(url_for('userdashboard'))


@app.route('/userbookings', methods =["GET", "POST"])
@login_required
def userbookings():
    bookings = Bookings.query.filter(Bookings.buser_id==current_user.user_id)
    data = []
    for book in bookings:

        ven = Venues.query.filter(book.bvenue_id==Venues.venue_id).first()
        sho = Shows.query.filter(book.bshow_id==Shows.show_id).first()
        data.append({"venue":ven.venue_name, "show":sho.show_name})
    return render_template('user_bookings.html', title='User Bookings', data=data)


@app.route('/newshow', methods =["GET", "POST"])
@login_required
def new_show():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = NewShowForm()

    if form.validate_on_submit():
        venue_id = int(form.venue.data[-1])
        show = Shows(show_name=form.showname.data, show_time=form.starttime.data, show_tag=form.tags.data, show_rating=form.ratings.data, show_price=form.price.data, svenue_id=venue_id)
        db.session.add(show)
        db.session.commit()
        flash('Show Created Successfully!!')
        return redirect(url_for('admindashboard'))
    return render_template('new_show.html', title='New Show', form=form)


@app.route('/newvenue', methods =["GET", "POST"])
@login_required
def new_venue():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = NewVenueForm()

    if form.validate_on_submit():
        venue = Venues(venue_name=form.venuename.data, venue_place=form.venueplace.data, venue_location=form.venueloc.data, venue_capacity=form.venuecap.data)
        db.session.add(venue)
        db.session.commit()
        flash('Venue Created Successfully!!')
        return redirect(url_for('admindashboard'))
    return render_template('new_venue.html', title='New Venue', form=form)


@app.route('/updateshow', methods =["GET", "POST"])
@login_required
def updateshow():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = UpdateShowForm()

    if form.validate_on_submit():
        sh_id = form.showid.data
        show = Shows.query.filter(Shows.show_id==sh_id).first()
        show.show_name=form.showname.data
        show.show_time=form.starttime.data
        show.show_tag=form.tags.data
        show.show_rating=form.ratings.data
        show.show_price=form.price.data
        db.session.commit()
        return redirect(url_for('admindashboard'))
    return render_template('update_show.html', title='Update Show', form=form)


@app.route('/updatevenue', methods =["GET", "POST"])
@login_required
def updatevenue():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = UpdateVenueForm()
    
    if form.validate_on_submit():
        ven_id = form.venueid.data
        venue = Venues.query.filter(Venues.venue_id==ven_id).first()
        venue.venue_name=form.venuename.data
        venue.venue_place=form.venueplace.data
        venue.venue_location=form.venueloc.data
        venue.venue_capacity=form.venuecap.data
        db.session.commit()
        return redirect(url_for('admindashboard'))
    return render_template('update_venue.html', title='Update Venue', form=form)


@app.route('/summary', methods =["GET", "POST"])
@login_required
def summary():
    venues = Venues.query.all()
    venu=[]
    for ven in venues:
        shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
        show=[]
        for sho in shows:
            rat = Ratings.query.filter_by(show_name=sho.show_name).all()
            avg_rating = 0.0
            count_rating = len(rat)
            if count_rating > 0:
                for r in rat:
                    avg_rating += r.ratings
                avg_rating = avg_rating/count_rating
            else:
                avg_rating = 0
            show.append({"name": sho.show_name, "showid": sho.show_id, "rating": avg_rating})
        venu.append({"name": ven.venue_name, "cards": show, "venueid": ven.venue_id})
    return render_template('summary.html', title='Summary', data=venu)


@app.route('/rate', methods =["GET", "POST"])
@login_required
def rating():
    form = RatingForm()

    if form.validate_on_submit():
        venue = form.venue.data
        show = form.show.data
        rating_value = form.rating.data
        userid = current_user.user_id
        rating_count = len(Ratings.query.all())+1
        rating = Ratings(ratings_id=rating_count, user_id=userid, show_name=show, venue_name=venue, ratings=rating_value)
        db.session.add(rating)
        db.session.commit()
        flash("Your rating has been saved")
        return redirect(url_for('userdashboard'))

    return render_template('rating.html', title='Ratings', form=form)


@app.route('/deleteshow', methods =["GET", "POST"])
@login_required
def deleteshow():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = UpdateShowForm()
    sh_id = form.showid.data
    show = Shows.query.filter(Shows.show_id==sh_id).first()
    db.session.delete(show)
    db.session.commit()
    flash('Deleted Successfully!!')
    print("successfully deleted")
    return redirect(url_for('admindashboard'))


@app.route('/deletevenue', methods =["GET", "POST"])
@login_required
def deletevenue():
    user = Users.query.filter_by(user_id = current_user.user_id).first()
    if not user.isAdmin():
        flash("You do not have sufficient access rights for this page!!")
        logout_clear()
        return redirect(url_for('index'))
    
    form = UpdateVenueForm()
    ve_id = form.venueid.data
    # print(form.venueid.data)
    venue = Venues.query.filter(Venues.venue_id==ve_id).first()
    db.session.delete(venue)
    db.session.commit()
    flash('Deleted Successfully!')
    print("successfully deleted")
    return redirect(url_for('admindashboard'))


@app.route('/deleteuser', methods =["GET", "POST"])
@login_required
def deleteuser():    
    us_id = current_user.user_id
    cur_user = Users.query.filter(Users.user_id==us_id).first()
    db.session.delete(cur_user)
    db.session.commit()
    flash('User Deleted Successfully!!')
    print("successfully deleted")
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_clear()
    flash("Logout Successful!!")
    return redirect(url_for('index'))


def logout_clear():
    session.clear()
    logout_user()

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8000)

# ------------------------------------------------------------------------------