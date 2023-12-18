# Database: src/db/__init__.py
from src.db.database import DataBase, get_db, close_db

# flask imports
from flask import (Blueprint, flash, g, render_template,
                   request, url_for, jsonify,
                   session, redirect
                   )

# login_required
from .user import login_required

from src.models import Proyecto

from src.schema import ProyectoDao
from src.models import GruposColaboradores
from src.schema import GruposColaboradoresDao

# Create the projects blueprint
bp = Blueprint('projects', __name__, url_prefix='/projects')

# create a route for the projects blueprint


@bp.route('/', methods=['GET'])
def index():
    return 'show all projects'


@bp.route('/<string:id>', methods=['GET'])
def view(id):
    try:
        # validate form data

        # database connection
        database = DataBase()

        # group dao
        proyecto_dao = ProyectoDao(
            database.connection, database.cursor)

        # get group by name
        project = proyecto_dao.get_by_id(id)

        if project is None:
            flash('The project does not exist.', 'error')
        else:
            # check if user is in group
            user_in_group = False

            if g.user != None:

                grupo_dao = GruposColaboradoresDao(
                    database.connection, database.cursor)

                user_in_group = grupo_dao.check_user_in_group(
                    g.user.id_usuario, project.group.id_grupo_colaboradores)

            # get projects by group

            database.close()

            return render_template('projects/view.html', project=project, user_in_group=user_in_group)

    except ValueError as error:
        flash(str(error), "error")

    except Exception as error:
        flash(str(error), "error")
        print(error)

    # show error 404
    return render_template('notFindPage.html', title='404 Group', message='Proyecto No Existe'), 404


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':

        try:

            proyecto = Proyecto()
            proyecto.nombre = request.form["nameProject"]
            proyecto.idea = request.form["ideaProject"]
            proyecto.presentacion = request.files["image_present"]
            proyecto.descripcion = request.form["description"]
            proyecto.fechaLimite = request.form["date_limit"]
            proyecto.presupuesto = request.form["budget"]
            proyecto.recompensa = request.form["reward"]
            proyecto.estado = "Activo"
            proyecto.metaAlcanzada = 0

            # generates
            proyecto.generateHashId()

            # name of the group
            grupo = request.form["nameGroup"]

            # database connection
            database = DataBase()

            # check if the name of the project exists

            grupo_dao = GruposColaboradoresDao(
                database.connection, database.cursor)

            if grupo_dao.check_name(grupo) == False:
                raise ValueError("The not exits the group name.")

            # get the id of the group

            grupo_dto = grupo_dao.get_by_name(grupo)

            print(grupo_dto.id_grupo_colaboradores)

            proyecto.group = grupo_dto

            # insert the group id in the project

            proyecto_dao = ProyectoDao(database.connection, database.cursor)

            if proyecto_dao.check_name(proyecto.nombre):
                raise ValueError("The project name already exists.")

            proyecto_dao.insert(proyecto)

            database.close()

            return redirect(url_for('user.profile'))

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            flash(str(error), "error")
            print(error)

    return render_template('projects/create.html')
