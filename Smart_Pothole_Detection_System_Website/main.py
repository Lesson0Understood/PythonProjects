from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed
from forms import CreateForm,UpdateForm, DeleteForm, LoginForm, RegisterForm
from functools import wraps
from helper_functions import print_all_data
from datetime import datetime

# ======================================================= Initializations ===============================================================


# Initializing app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "ISLAM"

# Initializing database
db = SQLAlchemy(app)

# Initializing authentication handler
login_manager = LoginManager(app)
login_manager.login_view = 'login_required_popup'

# Initializing roles handler
principal = Principal(app)
Admin_permission = Permission(RoleNeed("Admin"))


# Define global variables to use in html
@app.context_processor
def inject_user():
    return {'current_user': current_user}

# Example of setting the user in a before_request handler
@app.before_request
def before_request():
    user = current_user


# ======================================================= DataBase ===============================================================


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(100),default ="")

    def set_password(self,password):
        self.password = password

    def check_password(self,password):
        return self.password == password
    
    def get_roles(self):
        if self.roles:
            return self.roles.split(",")
        return []
    
    def has_role(self,role):
        return role in self.get_roles()
    
    def add_role(self,role):
        roles = self.get_roles()
        if role not in roles:
            roles.append(role)
            self.roles = ",".join(roles)
            db.session.commit()

    def remove_role(self,role):
        roles = self.get_roles()
        if role in roles:
            roles.remove(role)
            self.roles = ",".join(roles)
            db.session.commit()

    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.email}','{self.password}','{self.roles}')"


class Pothole(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    location = db.Column(db.String(100),nullable=False)
    severity = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)


    def __repr__(self):
        return f"pothole('{self.location}','{self.severity}','{self.image}')"


# ========================================================== Basic Pages =============================================================


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template("Basic_Pages/home.html",potholes=Pothole.query.all())


@app.route('/about')
def about():
    return render_template("Basic_Pages/about.html")


@app.route("/403")
def permission_error():
    return render_template("Errors/403.html")


@app.route('/map')
def map():
    potholes = Pothole.query.all()
    potholes_list = [
        {
            'id': pothole.id,
            'location': pothole.location,
            'severity': pothole.severity,
            'image_name': pothole.image
        }
        for pothole in potholes
    ]
    return render_template("Basic_Pages/map.html", potholes=potholes_list)


@app.route('/potholes')
def potholes():
    return render_template("Basic_Pages/potholes.html",potholes=Pothole.query.all(),id_to_img=id_to_img)


# ======================================================== Authentication =============================================================


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("User Already Registered", "warning")
            return redirect(url_for('register'))
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("User Registered Successfully", "success")
        return redirect(url_for("home"))
    return render_template('Authentication/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('User Already logged in',"info")
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('User Not Registered',"warning")
        elif not user.check_password(form.password.data):
            flash('Incorrect Password',"warning")
        else:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home"))
    return render_template('Authentication/login.html', form=form)


@app.route("/login_required")
def login_required_popup():
    if not current_user.is_authenticated:
        return render_template("Authentication/login_required.html")
    return redirect(url_for("home"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# defining a wrapper to handle permission checks on pages
def roles_required(roles):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.roles:
                return redirect(url_for("permission_error"))
            if set(roles).issubset({r for r in current_user.roles.split(",")}):
                return f(*args, **kwargs)
            return redirect(url_for("permission_error"))
        return wrapper

    return decorated_function


# ======================================================== potholes Related ===============================================================
def id_to_img(id):
    return f"images/Potholes/{id}.jpeg"

@app.route("/pothole/<int:pothole_id>")
@login_required
def pothole_detail(pothole_id):
    return render_template("potholes/pothole_detail.html",pothole=Pothole.query.get_or_404(pothole_id),pothole_id=pothole_id,id_to_img=id_to_img)


@app.route('/create',methods = ["GET","POST"])
@login_required
@roles_required(["Admin"])
def create_pothole():
    form = CreateForm()
    if form.validate_on_submit():
        pothole = Pothole()
        pothole.location = form.location.data
        pothole.severity = form.severity.data
        pothole.image = form.image.data
        db.session.add(pothole)
        db.session.commit()
        flash('Pothole Created Successfully',"success")
        return redirect(url_for("home"))
    return render_template("potholes/create.html", form=form)


@app.route('/update/<int:pothole_id>', methods=["GET", "POST"])
@login_required
@roles_required(["Admin"])
def update_pothole(pothole_id):
    pothole = Pothole.query.get_or_404(pothole_id)
    form = UpdateForm()

    if request.method == "POST":
        if form.validate_on_submit():
            pothole.location = form.location.data
            pothole.severity = form.severity.data
            pothole.image = form.image.data
            db.session.commit()
            flash('Pothole updated successfully!', 'success')
            return redirect(url_for("pothole_detail", pothole_id=pothole_id))
        else:
            flash('There was an error updating the pothole. Please check the form.', 'error')
    
    # For both GET requests and failed POST requests, set form data from pothole
    form.location.data = pothole.location
    form.severity.data = pothole.severity
    form.image.data = pothole.image
    
    return render_template("potholes/update.html", form=form, pothole=pothole)


@app.route('/delete/<int:pothole_id>',methods=["GET","POST"])
@login_required
@roles_required(["Admin"])
def delete_pothole(pothole_id):
    pothole = Pothole.query.get_or_404(pothole_id)
    form = DeleteForm(pothole)
    
    if form.validate_on_submit():
        db.session.delete(pothole)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("potholes/delete.html", form=form, pothole_id=pothole_id)


# =========================================================== Testing =============================================================

# I Used this for testing and debugging my website
@app.route('/test', methods=['GET'])
def create_test_user():
    print_all_data(db)
    if User.query.filter_by(email="islamcraft2007@gmail.com").first():
        return "Test user already exists"
    test_user = User(email="islamcraft2007@gmail.com", name="islam")
    test_user.set_password("a")
    test_user.add_role("Admin")
    db.session.add(test_user)
    db.session.commit()
    return "Test user created successfully"


# ======================================================== Run WebApp ==================================================================


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)