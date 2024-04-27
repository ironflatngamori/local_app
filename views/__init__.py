#!/usr/bin/python3
"""
defines the blueprints for the routes
"""
from flask import Blueprint
from config import __DB_FILE__

app_views = Blueprint('app_views', __name__, url_prefix='/')

from views.helper_views import *
from views.phases import *

