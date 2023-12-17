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

            # name of the group
            grupo = request.form["nameGroup"]

            # database connection
            database = DataBase()

            # check if the name of the project exists

            grupo_dao = GruposColaboradoresDao(database.conn, database.cursor)

            if grupo_dao.check_name(grupo):
                grupo_dto = grupo_dao.get_by_name(grupo)
                proyecto.group = grupo_dto

            proyecto_dao = ProyectoDao(database.conn, database.cursor)

            if proyecto_dao.check_name(proyecto.nombre):
                raise ValueError("The project name already exists.")

            proyecto_dao.insert(proyecto)

            return 'Project created successfully'

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            flash(str(error), "error")

        return 'Create project'
    return render_template('projects/create.html')
