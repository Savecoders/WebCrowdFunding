# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

# werkzeug security for password hashing
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from distutils.log import error

# flask imports
from flask import (Blueprint, flash, g, render_template,
                   request, url_for, jsonify,
                   session, redirect
                   )
from flask import current_app as app

# hash uid
import hashlib
import uuid
import functools

# imports models and schemas dao

from src.models import Usuario

from src.schema import UsuarioDao

# Create the user blueprint
# routes for user registration, login, and profile
bp = Blueprint('user', __name__, url_prefix='/user')

# Create the database object


# create a route for the user blueprint
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        try:
            # create user object
            usuario = Usuario()
            usuario.nombres = request.form['username']
            usuario.email = request.form['email']
            usuario.fecha_nacimiento = request.form['date_born']
            usuario.pais = request.form['country']
            usuario.ciudad = request.form['city']
            usuario.telefono = request.form['phone']
            usuario.image_perfil = request.files['image_profile']
            usuario.contrasena = request.form['password']
            usuario.generateEstado()
            usuario.generateHashPassword()
            usuario.generateHashId()

            # database connection
            db, c = get_db()

            # user dao
            usuario_dao = UsuarioDao(db, c)

            # insert user
            usuario_dao.insert(usuario)

            # close database connection
            close_db()

            return redirect(url_for('user.login'))

        except ValueError as error:
            # imprimir error
            flash(str(error))

        except Exception as error:
            # imprimir error
            flash(str(error))

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


@bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':

        db, c = get_db()

        user = Usuario()
        user.nombres = 'test'
        user.email = 'test@gmail.com'
        user.fecha_nacimiento = '2003-05-05'
        user.pais = 'ecuador'
        user.ciudad = 'quito'
        user.telefono = '0987654321'
        with open('public/static/img/profile.jpg', 'rb') as file:
            user.image_perfil = file.read()
        user.contrasena = 'password'
        user.generateEstado()
        user.generateHashId()
        user.generateHashPassword()

        user_dao = UsuarioDao(db, c)
        user_dao.insert(user)
        return 'Create user'
    return render_template('user/update.html')


@bp.route('/profile', methods=['GET'])
def profile():
    return 'Profile'
