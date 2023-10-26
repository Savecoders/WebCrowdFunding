
from flask import Blueprint, request, render_template, url_for, session

# Create the user blueprint
bp = Blueprint('user', __name__, url_prefix='/user')

# create a route for the user blueprint


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'Create user'
    return render_template('user/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Login user'
    return render_template('user/login.html')


@bp.route('/profile', methods=['GET'])
def profile():
    return 'Profile'
