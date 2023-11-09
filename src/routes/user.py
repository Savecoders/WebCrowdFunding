# Database: src/db/__init__.py
from src.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (Blueprint, flash, g, render_template, request, url_for,
                   session, redirect)
from flask import current_app as app
from werkzeug.exceptions import abort
import functools
# Create the user blueprint
# routes for user registration, login, and profile
bp = Blueprint('user', __name__, url_prefix='/user')

# Create the database object


# create a route for the user blueprint
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['mail']
        date_born = request.form['date_born']
        country = request.form['country']
        city = request.form['city']
        phone = request.form['phone']
        password = request.form['password']

    return render_template('user/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Login user'
    return render_template('user/login.html')


@bp.route('/update', methods=['GET'])
def update():
    if request.method == 'POST':
        return 'Create user'
    return render_template('user/update.html')


@bp.route('/profile', methods=['GET'])
def profile():
    return 'Profile'
