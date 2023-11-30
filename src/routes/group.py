
# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

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
def index():
    return 'show all groups'


@login_required
@bp.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # get form data

        try:

            name = request.form['name']
            # validate form data

            # create group object
            grupo = GruposColaboradores()
            grupo.nombre = name

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

        except ValueError as e:
            flash(e, 'error')

        except Exception as e:
            flash(e, 'error')

    return render_template('group/create.html')


@login_required
@bp.route('/add-user-to-group', methods=['GET', 'POST'])
def add_user():
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
                    flash('No se ha creado un grupo', 'error')

                # insert user to group

                grupo_dao.insert_user(
                    user.id_usuario, grupo.id_grupo_colaboradores)

            else:
                flash('No se ha creado un grupo', 'error')

        except ValueError as e:

            flash(e, 'error')

        except Exception as e:

            flash(e, 'error')

    return render_template('group/create.html')
