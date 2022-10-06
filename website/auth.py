from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re




auth = Blueprint('auth', __name__)

@auth.route('/settings/password', methods=['GET', 'POST'])
@login_required
def update_password():
    if request.method == 'POST':
        cpassword = request.form.get('cpassword')
        npassword = request.form.get('npassword')
        if check_password_hash(current_user.password, cpassword):
            current_user.password=generate_password_hash(npassword, method='sha256')
            db.session.commit()
            flash('Informations Are Updated successfully!', category='success')
            return redirect(url_for('views.settings'))
        else:
         flash('The password you’ve entered is incorrect.', category='error')

    return render_template("update_password.html", user=current_user)

@auth.route('/settings/username', methods=['GET', 'POST'])
@login_required
def update_username():
    if request.method == 'POST':
        nusername = request.form.get('nusername')
        
        if nusername:
           current_user.first_name=nusername
           db.session.commit()
           flash('Informations Are Updated successfully!', category='success')
           return redirect(url_for('views.settings'))
        else:
            flash('Please Enter A Valid Username!', category='error')

    return render_template("update_username.html", user=current_user)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        regex=r'\b[A-Za-z0-9._%+-]+@[draexlmaier]+\.[A-Z|a-z]{2,}\b'

        user = User.query.filter_by(email=email).first()
        if not (re.fullmatch(regex, email)):
         flash('You must use @draexlmaier Mail .', category='error')

        elif user:
            flash('Email already exists.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email,first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created Successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)
