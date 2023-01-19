from flask import Flask, render_template, request, redirect, url_for, flash, abort
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreateItemForm, RegistrationForm, LoginForm
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
import os

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

my_email = os.environ['my_email']
password = os.environ['password']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["app.config['secret_key']"]
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    items = relationship("Item", back_populates="author")

class Item(db.Model):
    __tablename__ = "portfolio-items"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="items")

    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    github = db.Column(db.String(250), nullable=False)
    dribbble = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


@app.route('/')
def home():
    items = Item.query.all()
    return render_template("index.html")

@app.route('/portfolio')
def portfolio():
    items = Item.query.all()
    return render_template("portfolio.html", all_items=items, current_user=current_user)


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name} \nEmail: {email} \nPhone: {phone} \nMessage: {message} "
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(my_email, my_email, email_message)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password=form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/artifact/<int:item_id>', methods=["GET", "POST"])
def show_item(item_id):
    requested_item = Item.query.get(item_id)
    return render_template("item.html", item=requested_item, current_user=current_user)


@app.route("/new-item", methods=["GET", "POST"])
@admin_only
def add_new_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        new_item = Item(
            author=current_user,
            title=form.title.data,
            description=form.description.data,
            img_url=form.img_url.data,
            github=form.github.data,
            dribbble=form.dribbble.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_item.html", form=form, current_user=current_user)

@app.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
@admin_only
def new_item(item_id):
    item = Item.query.get(item_id)
    edit_form = CreateItemForm(
        title=item.title,
        img_url=item.img_url,
        description=item.description,
        github=item.github,
        dribbble=item.dribbble)

    if edit_form.validate_on_submit():
        item.title = edit_form.title.data
        item.img_url = edit_form.img_url.data
        item.description = edit_form.description.data
        item.github = edit_form.github.data
        item.dribbble = edit_form.dribbble.data
        db.session.commit()
        return redirect(url_for("show_item", item_id=item.id))
    return render_template("new_item.html", form=edit_form, is_edit=True, current_user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
