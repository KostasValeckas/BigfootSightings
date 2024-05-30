from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user

from BigfootSightings.forms import UserLoginForm, UserSignupForm, BackToMainForm
from BigfootSightings.queries import get_user_by_user_name , insert_user
from BigfootSightings.models import User

Login = Blueprint('Login', __name__)


@Login.route("/")
@Login.route("/home")
def home():
    return render_template('pages/home.html')

@Login.route("/backToMainFromSignup", methods=['GET', 'POST'])
def backToMainFromSignup():
    form = BackToMainForm()
    if request.method == 'POST':
            if form.validate_on_submit():
                return redirect(url_for('Login.home'))

    return render_template('pages/signup-landing.html', form=form)

@Login.route("/backToMainFromLogin", methods=['GET', 'POST'])
def backToMainFromLogin():
    form = BackToMainForm()
    if request.method == 'POST':
            if form.validate_on_submit():
                return redirect(url_for('Login.home'))

    return render_template('pages/login-landing.html', form=form)


@Login.route("/about")
def about():
    return render_template('pages/about.html')


@Login.route("/style-guide")
def style_guide():
    return render_template('pages/style-guide.html')


@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = get_user_by_user_name(username)
            if user and password == form.password.data:
                print("pre-login: ", user.is_authenticated())
                login_user(user, remember=True)
                print("post-login: ", user.is_authenticated())
                next_page = request.args.get('next')
                print(next_page)
                return redirect(next_page) if next_page else redirect(url_for('Login.backToMainFromLogin'))
    print("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
    return render_template('pages/login.html', form=form)


@Login.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserSignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            user = get_user_by_user_name(form.username.data)
            
            if (user is None and \
                (form.password.data == form.password_repeat.data)):
            
                user_data = {
                    'username': form.username.data,
                    'password': form.password.data
                }
                
                user = User(user_data)
                
                insert_user(user)

                user = get_user_by_user_name(form.username.data)

                if user:
                    login_user(user, remember=True)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('Login.backToMainFromSignup'))
    return render_template('pages/signup.html', form=form)


@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.login'))
