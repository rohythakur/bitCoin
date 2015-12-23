from flask import render_template, redirect, url_for, flash, request, session, g
from flask.ext.login import current_user, logout_user, flash, login_user
from . import auth
from .. import db
from ..models import User

from .forms import ChangePasswordForm, RegistrationForm, LoginForm
from sqlalchemy.orm.exc import UnmappedInstanceError




@auth.before_request
def before_request():
    g.user = current_user



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                print (user)
                return redirect(url_for('main.home'))

            flash('Invalid username or password.')



    return render_template('auth/login.html', form=form)



@auth.route('/register', methods=['GET', 'POST'])
def register():
    print "step 1 register"
    form = RegistrationForm()
    if request.method == 'POST':
        print "step 2 register"
        user = User(username=form.username.data,
                    password=form.password.data,
                    welcomeMessage=form.welcomeM.data,
                    pin=form.pin.data)
        db.session.add(user)
        print "step 3 register"
        db.session.commit()


        flash('Logged in Successfully')
        return redirect(url_for('auth.login'))
    return render_template('/auth/register.html', form=form)



@auth.route('/security/<username>', methods=['GET', 'POST'])
def security(username):
    form = ChangePasswordForm()
    user = User.query.filter_by(username=username).first()
    print ("here")
    if form.validate_on_submit():
         if current_user.verify_password(form.old_password.data):

            print ("info updated")
            user.password = form.password.data
            user.welcomeMessage = form.welcomeM.data

            db.session.add(user)
            db.session.commit()
            print ("info updated")

            return redirect(url_for('main.home'))
    return render_template('/auth/security.html', user=user, form=form)



@auth.route('/logout')
def logout():
    try:
       g.user.authenticated = False
       db.session.add(g.user)
       db.session.commit()
    except UnmappedInstanceError:
       pass
