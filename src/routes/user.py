# Database: src/db/__init__.py
from src.db.database import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (Blueprint, flash, g, render_template, request, url_for,
                   session, redirect)
from flask import current_app as app
from werkzeug.exceptions import abort
from distutils.log import error
import functools
# hash uid
import hashlib
import uuid
# Create the user blueprint
# routes for user registration, login, and profile
bp = Blueprint('user', __name__, url_prefix='/user')

# Create the database object


# create a route for the user blueprint
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['email']
        date_born = request.form['date_born']
        country = request.form['country']
        city = request.form['city']
        phone = request.form['phone']
        password = request.form['password']

        id = hashlib.sha256(uuid.uuid4().bytes).hexdigest()

        db, c = get_db()

        error = None

        if not username:
            error = 'Username is required'

        elif not password:
            error = 'Password is required'

        elif not mail:
            error = 'Mail is required'

        elif not date_born:
            error = 'Date born is required'

        elif not country:
            error = 'Country is required'

        elif not city:
            error = 'City is required'

        elif not phone:
            error = 'Phone is required'

        if error is None:

            c.execute("SELECT * FROM USUARIO")

            sql = 'INSERT INTO USUARIO(id, username, password, mail, date_born, country, city, phone) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'

            values = (id, username, generate_password_hash(password),
                      mail, date_born, country, city, phone)

            c.execute(sql, values)
            db.commit()
            return redirect(url_for('user.login'))

    return render_template('user/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db, c = get_db()
        error = None

        c.execute(
            'select * from USUARIO where mail = :1', (email,)
        )

        user = c.fetchone()

        if user is None:
            error = 'Invalid password or mail'
        elif not check_password_hash(user['password'], password):
            error = 'Invalid password or mail'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('/'))
        flash(error)
    return render_template('user/login.html')


@bp.route('/update', methods=['GET'])
def update():
    if request.method == 'POST':
        return 'Create user'
    return render_template('user/update.html')


@bp.route('/profile', methods=['GET'])
def profile():
    return 'Profile'
