from flask import render_template, redirect, url_for, g, flash, request, session
from flask.ext.login import logout_user, current_user, login_required, login_user
from . import main
from .forms import EditProfileForm
from .. import db
from ..models import User
from app import login_manager, app


from sqlalchemy.orm.exc import UnmappedInstanceError



@app.before_request
def before_request():
    g.user = current_user




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    print 'Should be running this index'

    return render_template('index.html')


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    form = EditProfileForm(request.form, obj=current_user)
    user = User.query.filter_by(username=username).first()
    print("user profile page")

    if request.method == 'POST':
        form.populate_obj(user)
        user.welcomeMessage = form.welcomeM.data
        user.about_me = form.about_me.data


        print "step 3 register"
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.home'))



    return render_template('/main/profile.html', user=user, form=form)












@main.route('/showtrades', methods=['GET', 'POST'])
def buysell():
    return render_template('main/buysell.html')

@main.route('/home', methods=['GET', 'POST'])
def home():

    return render_template('main/home.html')


@main.route('/auth/index', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    logout_user()
    g.user.authenticated = False
    print ("sucessfully logged out")
    return redirect(url_for('auth.login'))




@main.route('/termsofservice')
def tos():
    return render_template('main/tos.html')




@main.route('/aboutus')
def about():
    return render_template('main/about.html')



@main.route('/contact')
def contact():
    return render_template('main/contact.html')


@main.route('/faq')
def faq():
    return render_template('main/faq.html')