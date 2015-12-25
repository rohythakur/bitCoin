__author__ = 'eeamesX'
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db, login_manager




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(64), unique=True, index=True)
    password_hash  = db.Column(db.String(128))
    welcomeMessage = db.Column(db.String(64))
    about_me       = db.Column(db.Text())
    pgpkey         = db.Column(db.Text())
    pin            = db.Column(db.Integer)




    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)



    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])




class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(UserMixin, db.Model):
    __tablename__ = 'trades'
    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyorsell         = db.Column(db.String(64))
    payment_method    = db.Column(db.String(64), unique=False, index=True)
    location          = db.Column(db.String(128))
    person            = db.Column(db.String(64))
    item_listed       = db.Column(db.Boolean)
    item_description  = db.Column(db.Text())
    price             = db.Column(db.Integer)
    tradelimitmin     = db.Column(db.Integer)
    tradelimitmax     = db.Column(db.Integer)
    selectbox         = db.Column(db.Boolean)


