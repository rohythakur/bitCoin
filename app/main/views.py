from flask import render_template, redirect, url_for, g, flash, request, session
from flask.ext.login import logout_user, current_user, login_required, login_user
from . import main
from .forms import EditProfileForm, CreateItemForm, FindMoneyForm
from .. import db
from ..models import User, Item
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



@main.route('/posttrade', methods=['GET', 'POST'])
@login_required
def createitem():
    form = CreateItemForm(request.form, obj=current_user)
    items = Item.query.all()
    print items
    form.buyorsell.choices= [('sell', 'Sell'),('buy', 'Buy')]
    form.location.choices= [('tor', 'Torland'),('NA', 'North America'), ('SA', 'South America'),
                            ('Europe', 'Europe'), ('Asia', 'Asia'), ('AU', 'Australia'), ('Russia', 'Russia')]
    form.payment_method.choices=[(c, c) for c in ['Cash By Mail', 'Cash Deposit',
                                                  'Moneygram', 'Amazon Gift Card', 'WalMart Gift Card',
                                                  'PayPal', 'PayPal Mycash', 'Vanilla',
                                                  'Google Wallet', 'Postal Order',
                                                  'Cashiers Check', 'Other Gift Card', 'Gold']]
    print ("Create Item Page")
    if request.method == 'POST':
        items = Item(payment_method=form.payment_method.data,
                    buyorsell=form.buyorsell.data,
                    location=form.location.data,
                    item_listed=form.item_listed.data,
                    item_description=form.item_description.data,
                    price = form.price.data,
                    person = current_user.username,
                    tradelimitmin=form.tradelimitmin.data,
                    tradelimitmax=form.tradelimitmax.data
                    )

        db.session.add(items)
        db.session.commit()
        print ("Add Created")

        return redirect(url_for('main.createitem'))
    return render_template('main/postTrade.html', form=form, user=user)




@main.route('/delete/<int:id>', methods=['DELETE', 'POST'])
def deleteid(id):
    object = Item.query.get_or_404(id)
    delete(object)
    return redirect(url_for('index'))




@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = CreateItemForm()
    form.selectchoice.choices= [('sell', 'Sell'),('buy', 'Buy')]
    trades = Item.query.filter(Item.person==g.user.username).all()
    if form.validate_on_submit():
        print selectchoice

    return render_template('main/dashboard.html', trades=trades, form=form)





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



@main.route('/viewperson/<username>', methods=['GET', 'POST'])
def viewperson(username):

    user = User.query.filter_by(username=username).first()
    trades = Item.query.filter_by(person=user.username).all()

    return render_template('main/viewperson.html', user=user, trades=trades)



@main.route('/showtrades/', methods=['GET', 'POST'])
def buysell():
    form = FindMoneyForm()
    form.buyorsell.choices= [('sell', 'Sell'),('buy', 'Buy')]
    form.payment_method.choices=[(c, c) for c in ['Cash By Mail', 'Cash Deposit',
                                                  'Moneygram', 'Amazon Gift Card', 'WalMart Gift Card',
                                                  'PayPal', 'PayPal Mycash', 'Vanilla',
                                                  'Google Wallet', 'Postal Order',
                                                  'Cashiers Check', 'Other Gift Card', 'Gold']]
    x='buy'
    s ='sell'
    trades = Item.query.filter(Item.buyorsell==x or Item.buyorsell==s).all()
    if request.method == "POST":
        print form.buyorsell.data,
        print form.payment_method.data,


    return render_template('main/buysell.html', user=user, trades=trades, form=form)








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