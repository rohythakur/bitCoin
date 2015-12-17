__author__ = 'eeamesX'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views