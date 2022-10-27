from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm
from .models import User, db
import hashlib
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/userProfile")
def userProfile():
    return render_template('test.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/userSettings")
def userSettings():
    return render_template('settings.html')


@app.route("/community")
def communityPage():
    return render_template('community.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Login successful ${current_user.email}', 'success')
        return redirect(url_for('home'))
        

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            flash(f'Login successful ${current_user.email}', 'success')
            next_page = request.args.get('next')
        
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong Password", "Danger")

    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        
        checkUsername = User.query.filter_by(username=form.username.data).first()
        if checkUsername:
            flash("Username already taken", "Danger")
            return redirect(url_for('register'))
        checkEmail = User.query.filter_by(email=form.email.data).first()
        if checkEmail:
            flash("Email already taken", "Danger")
            return redirect(url_for('register'))


        db.session.add(user)
        db.session.commit()
        test = db.get_or_404(User, 1)
        flash(test.username+" "+test.email+" "+test.password, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

