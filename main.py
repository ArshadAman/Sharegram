from flask import Flask
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
db = SQLAlchemy(app)


#Login Feature
# login_manager = LoginManager()

# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))













@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_user():
    return render_template("login.html")

@app.route("/register")
def register_user():
    return render_template("register.html")








if __name__ == '__main__':
    app.run(debug=True)