__author__ = 'ed'
from functools import wraps
from flask import abort, session, flash, redirect, url_for, request, g
from flask.ext.login import current_user




def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_anonymous():
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('main.index'))
    return wrap