
# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

# date time
import datetime

# flask imports
from flask import (Blueprint, request, render_template,
                   url_for, session, g, flash, redirect)

# imports models and schemas dao

from src.models import GruposColaboradores, Usuario

from src.schema import GruposColaboradoresDao, UsuarioDao, ProyectoDao


# login_required
from .user import login_required

# Create the group blueprint

bp = Blueprint('group', __name__, url_prefix='/group')

# create a route for the group blueprint


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

            # get projects by group

            proyecto_dao = ProyectoDao(database.connection, database.cursor)

            projects = proyecto_dao.get_projects_by_group(
                grupo.id_grupo_colaboradores)

            # close database connection
            database.close()

            return render_template('group/view.html', grupo=grupo, user_in_group=user_in_group, projects=projects)

    except ValueError as e:
        flash(str(e), 'error')

    except Exception as e:
        flash(str(e), 'error')

    # show error 404
    return render_template('notFindPage.html', title='404 Group', message='Grupo No Existe'), 404


@bp.route('/', methods=['GET'])
def all_group():

    # database connection
    database = DataBase()

    # group dao

    grupo_dao = GruposColaboradoresDao(
        database.connection, database.cursor)

    # get all groups

    grupos = grupo_dao.get_all()

    # close database connection
    database.close()

    return render_template('group/index.html', groups=grupos)


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

            # close database connection
            database.close()

            flash('The group was created successfully.', 'success')

            return redirect(url_for('user.profile'))

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            flash(str(error), "error")

    return render_template('group/create.html')


@bp.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    try:

        # get group by id
        database = DataBase()

        grupo_dao = GruposColaboradoresDao(
            database.connection, database.cursor)

        grupo = grupo_dao.get_by_id(id)

        if grupo is None:
            raise ValueError("The group does not exist.", "error")

        if request.method == 'POST':
            # get form data

            name = request.form['name']
            description = request.form['descripcion']
            image = request.files['image_profile']

            # create group object
            grupo.nombre = name
            grupo.descripcion = description
            grupo.imagen = image

            # update group
            grupo_dao.update(grupo)

            # close database connection
            database.close()

            flash('The group was updated successfully.', 'success')

            return redirect(url_for('group.index', id=id))

        # close database connection
        database.close()
        return render_template('group/edit.html', grupo=grupo)

    except ValueError as error:
        flash(str(error), "error")


@bp.route('/adduser/<string:id>', methods=['POST'])
@login_required
def add_user(id):
    if request.method == 'POST':
        try:
            email = request.form['email']

            # database connection
            database = DataBase()

            # user exists

            usuario_dao = UsuarioDao(database.connection, database.cursor)

            usuario = usuario_dao.get_by_email(email)

            if usuario is None:
                raise ValueError("The user does not exist.")

            # get group

            grupo_dao = GruposColaboradoresDao(
                database.connection, database.cursor)

            grupo = grupo_dao.get_by_id(id)

            if grupo is None:
                raise ValueError("The group does not exist.")

            # add user to group

            grupo_dao.insert_user(usuario.id_usuario,
                                  grupo.id_grupo_colaboradores)

            # close database connection
            database.close()

            flash("The user was added to the group successfully.", "success")

            return redirect(url_for('group.index', id=id))

        except ValueError as error:

            flash(str(error), "error")

        except Exception as e:

            flash(str(error), "error")

    return redirect(url_for('group.index', id=id))


@bp.route('/removeuser/<string:id_grupo>/<string:id_usuario>', methods=['POST'])
@login_required
def remove_user(id_grupo, id_usuario):
    if request.method == 'POST':
        try:

            database = DataBase()
            usuario_dao = UsuarioDao(database.connection, database.cursor)

            # user exists

            usuario = usuario_dao.get_by_id(id_usuario)

            if usuario is None:
                raise ValueError("The user does not exist.")

            # get group

            grupo_dao = GruposColaboradoresDao(
                database.connection, database.cursor)

            grupo = grupo_dao.get_by_id(id_grupo)

            if grupo is None:
                raise ValueError("The group does not exist.")

            # remove user to group

            grupo_dao.remove_user(usuario.id_usuario,
                                  grupo.id_grupo_colaboradores)

            # close database connection
            database.close()

            flash("The user was removed to the group successfully.", "success")

            return redirect(url_for('group.index', id=id_grupo))

        except ValueError as error:

            flash(str(error), "error")

        except Exception as e:

            flash(str(error), "error")

    return redirect(url_for('group.index', id=id_grupo))
