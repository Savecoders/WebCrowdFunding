
# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

# date time
import datetime

# flask imports
from flask import Blueprint, request, render_template, url_for, session, g, flash

# imports models and schemas dao

from src.models import GruposColaboradores

from src.schema import GruposColaboradoresDao

from src.models import Usuario

from src.schema import UsuarioDao

# login_required
from .user import login_required

# Create the group blueprint

bp = Blueprint('group', __name__, url_prefix='/group')

# create a route for the group blueprint


@bp.route('/', methods=['GET'])
def all_group():
    return 'show all groups'


@bp.route('/<string:id>', methods=['GET'])
def index(id):
    try:
        # validate form data

        # database connection
        database = DataBase()

        # group dao
        grupo_dao = GruposColaboradoresDao(
            database.connection, database.cursor)

        # get group by name
        grupo = grupo_dao.get_by_id(id)

        grupo.load_image()

        if grupo is None:
            flash('The group does not exist.', 'error')
        else:

            # check if user is in group
            user_in_group = False

            if g.user != None:
                user_in_group = grupo_dao.check_user_in_group(
                    g.user.id_usuario, grupo.id_grupo_colaboradores)

            grupo.usuario_grupos = grupo_dao.get_users_by_group(
                grupo.id_grupo_colaboradores)

            return render_template('group/view.html', grupo=grupo, user_in_group=user_in_group)

    except ValueError as e:
        flash(str(e), 'error')

    except Exception as e:
        flash(str(e), 'error')

    # show error 404
    return render_template('notFindPage.html', title='404 Group', message='Grupo No Existe'), 404


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # get form data
        try:

            name = request.form['name']
            description = request.form['descripcion']
            image = request.files['image_profile']

            # generate date

            date = datetime.date.today()

            # convert date to string

            date = date.strftime("%d-%m-%Y")

            # create group object
            grupo = GruposColaboradores()
            grupo.nombre = name
            grupo.descripcion = description
            grupo.imagen = image
            grupo.fecha_creacion = date

            # generate hash id
            grupo.generate_hash_id()

            # database connection
            database = DataBase()

            # group dao
            grupo_dao = GruposColaboradoresDao(
                database.connection, database.cursor)

            # insert group
            grupo_dao.insert(grupo)

            # insert the user create

            grupo_dao.insert_user(
                g.user.id_usuario, grupo.id_grupo_colaboradores)

            g.last_inserted_id = grupo.id_grupo_colaboradores

            flash('The group was created successfully.', 'success')

            return render_template(url_for('user.profile'))

        except ValueError as e:
            flash(e, 'error')

        except Exception as e:
            flash(e, 'error')

    return render_template('group/create.html')


@login_required
@bp.route('/<string:name>/add-users', methods=['GET', 'POST'])
def add_user(name):
    if request.method == 'POST':

        try:
            # get from data
            mail = request.form['email']

            # validate form data

            # database connection
            database = DataBase()

            # user dao
            user_dao = UsuarioDao(database.connection, database.cursor)

            # get user by mail
            user = user_dao.get_by_email(mail)

            # group dao

            if g.last_inserted_id != None:

                grupo_dao = GruposColaboradoresDao(
                    database.connection, database.cursor)

                grupo = grupo_dao.get_by_id(g.last_inserted_id)

                if grupo is None:
                    flash('Not create a group', 'error')

                # insert user to group

                grupo_dao.insert_user(
                    user.id_usuario, grupo.id_grupo_colaboradores)

            else:
                flash('Not create a group', 'error')

        except ValueError as e:

            flash(e, 'error')

        except Exception as e:

            flash(e, 'error')

    return render_template('group/create.html')
