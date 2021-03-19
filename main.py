from enum import unique
import re
from flask import Flask, redirect,url_for, flash
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
# from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, current_user, logout_user
from flask.templating import render_template
from flask_bootstrap import Bootstrap
from flask_bootstrap.forms import render_form

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Login Feature
login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(100), nullable = False)

db.create_all()



@app.route("/")
def home():
    return render_template("index.html", current_user=current_user)

@app.route("/register", methods=["POST","GET"])
def register_user():
    if request.method == "POST":
        email = request.form.get('signup-email')
        password = request.form.get('signup-password')
        name = request.form.get('signup-name')
        username = request.form.get('signup-username')

        if User.query.filter_by(username=username).first():  # if a user is found, we want to redirect back to signup page so user can try again
            flash('User already exists')
            return redirect(url_for('register_user'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256', salt_length=8), username=username)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    
    return render_template("register.html", current_user=current_user)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("login_username")
        password = request.form.get("login_password")

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("That username does not exit")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", current_user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user= current_user)









if __name__ == '__main__':
    app.run(debug=True)