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
            database = DataBase()

            # user dao
            usuario_dao = UsuarioDao(database.connection, database.cursor)

            # insert user
            usuario_dao.insert(usuario)

            # close database connection
            database.close()

            return redirect(url_for('user.login'))

        except ValueError as error:
            # imprimir error
            print(error)
            flash(str(error))

        except Exception as error:
            # imprimir error
            print(error)
            flash(str(error))

    return render_template('user/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form data
        email = request.form['email']
        password = request.form['password']

        database = DataBase()

        # capture error

        error = None

        usuario_dao = UsuarioDao(database.connection, database.cursor)

        user = usuario_dao.get_by_email(email)

        # close database connection
        database.close()

        if user is None:
            error = 'Invalid password or mail'
        elif not check_password_hash(user.contrasena, password):
            error = 'Invalid password or mail'

        if error is None:
            session.clear()
            session['id_usuario'] = user.id_usuario
            return redirect(url_for('user.profile'))
        flash(error)
    return render_template('user/login.html')


@bp.before_app_request
def load_logged_in_user():

    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        g.user = None
    else:
        database = DataBase()

        usuario_dao = UsuarioDao(database.connection, database.cursor)

        user = usuario_dao.get_by_id(id_usuario)

        user.load_image_perfil()

        g.user = user


def login_required(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapper_view


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':

        password = request.form['password']

        try:
            # create user object
            last_user = g.user

            error = None

            if not check_password_hash(last_user.contrasena, password):
                error = 'Invalid password'

            if error is None:

                # using the last user

                last_user.nombres = request.form['username']
                last_user.email = request.form['email']
                last_user.fecha_nacimiento = request.form['date_born']
                last_user.pais = request.form['country']
                last_user.ciudad = request.form['city']
                last_user.telefono = request.form['phone']
                last_user.image_perfil = request.files['image_profile']

                # database connection
                database = DataBase()

                # user dao
                usuario_dao = UsuarioDao(database.connection, database.cursor)

                # update user
                usuario_dao.update_basic_info(last_user)

                # close database connection
                database.close()

                # update session

                session.clear()
                session['id_usuario'] = last_user.id_usuario
                return redirect(url_for('user.profile'))

            flash(error)

        except ValueError as error:
            # imprimir error
            print(error)
            flash(str(error))

        except Exception as error:
            # imprimir error
            print(error)
            flash(str(error))

    return render_template('user/update.html')


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('user/profile.html')


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))
